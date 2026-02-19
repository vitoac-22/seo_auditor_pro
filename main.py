import os
import sys
from modules.scraper import SiteScraper
from modules.market_data import MarketData
from modules.analyzer import SEOAnalyzer
from modules.reporter import StrategicReport

def load_seeds(filepath="seeds.txt"):
    """Carga semillas evitando líneas vacías."""
    if not os.path.exists(filepath):
        print(f"   [Error] Archivo {filepath} no encontrado.")
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]

def main():
    print("\n=================================================")
    print("   AUDITORÍA SEO 360° | REY SABIO SALOMÓN")
    print("   Protocolo: Scraping Quirúrgico + Análisis de Densidad")
    print("=================================================\n")
    
    # 1. OBJETIVOS (Tus URLs Reales)
    TARGETS = {
        "Inicio (Home)": "https://www.reysabiosalomon.org/",
        "Básica (Elemental)": "https://www.reysabiosalomon.org/basicaelemental",
        "Bachillerato": "https://www.reysabiosalomon.org/basicamediaysuperior",
        "Nosotros": "https://www.reysabiosalomon.org/about-us"
    }

    # 2. COMPETENCIA (URLs Profundas para obtener texto real)
    COMPETITORS = [
        "https://www.ism.edu.ec/admisiones/",
        "https://www.jkepler.edu.ec/admisiones/",
        "https://www.einstein.k12.ec/admisiones/"
    ]
    
    # 3. CARGA DE DATOS
    seeds = load_seeds("seeds.txt")
    if not seeds: return

    print(f"> FASE 1: Inteligencia de Mercado")
    market = MarketData()
    # Usamos sugerencias para ampliar el vocabulario semántico
    all_keywords = market.get_suggestions(seeds)
    # Aseguramos que las semillas originales estén incluidas con prioridad
    final_keyword_list = list(set(seeds + all_keywords))
    print(f"   Vocabulario objetivo expandido a {len(final_keyword_list)} términos.")

    scraper = SiteScraper("") # Instancia genérica
    
    # 4. AUDITORÍA INTERNA (Scraping Limpio)
    print(f"\n> FASE 2: Escaneo Quirúrgico Interno")
    site_corpus = {}
    for name, url in TARGETS.items():
        print(f"   Analizando: {name}")
        scraper.url = url
        data = scraper.audit()
        # Solo agregamos si hay contenido real detectado
        if data and data.get('content_sample') and len(data['content_sample']) > 50:
            site_corpus[name] = data['content_sample']
        else:
            print(f"      [!] Advertencia: {name} parece vacía o protegida.")

    if not site_corpus:
        print("   [FATAL] No se pudo extraer contenido válido. Revisa el Scraper.")
        return

    # 5. ANÁLISIS COMPETENCIA
    print(f"\n> FASE 3: Deconstrucción de Competencia")
    competitor_corpus = {}
    for url in COMPETITORS:
        scraper.url = url
        try:
            data = scraper.audit()
            if data and data.get('content_sample'):
                competitor_corpus[url] = data['content_sample']
        except:
            print(f"   [X] Fallo al leer {url}")
    print(f"   Datos extraídos de {len(competitor_corpus)} competidores.")

    # 6. PROCESAMIENTO MATEMÁTICO
    print("\n> FASE 4: Cálculo de Matrices de Relevancia")
    analyzer = SEOAnalyzer(site_corpus, final_keyword_list)
    
    # A) Matriz Interna
    df_results = analyzer.run_matrix_analysis()
    
    # B) Matriz Competencia
    comp_keywords = analyzer.analyze_competitors(competitor_corpus)

    # 7. GENERACIÓN DEL ENTREGABLE
    print("\n> FASE 5: Generación de Reporte Ejecutivo")
    if df_results is not None:
        reporter = StrategicReport()
        reporter.generate(
            df_results, 
            "output/heatmap_estrategico.png", 
            comp_keywords, 
            "output/Auditoria_SEO_Final.pdf"
        )
    
    print("\n=================================================")
    print("   ¡AUDITORÍA COMPLETADA!")
    print("   Abre el archivo: output/Auditoria_SEO_Final.pdf")
    print("=================================================")

if __name__ == "__main__":
    main()