# UBICACIÓN: main.py
import os
import sys
from modules.scraper import SiteScraper
from modules.market_data import MarketData
from modules.analyzer import SEOAnalyzer
from modules.reporter import StrategicReport

def load_seeds(filepath="seeds.txt"):
    if not os.path.exists(filepath):
        print(f"   [Error] Crea el archivo {filepath} primero.")
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]

def main():
    print("\n=================================================")
    print("   AUDITORÍA SEO: PROTOCOLO CONSULTORÍA V2.0")
    print("=================================================\n")
    
    # 1. OBJETIVOS (Tus URLs)
    TARGETS = {
        "Home": "https://www.reysabiosalomon.org/",
        "Basica": "https://www.reysabiosalomon.org/basicaelemental",
        "Bachillerato": "https://www.reysabiosalomon.org/basicamediaysuperior",
        "Nosotros": "https://www.reysabiosalomon.org/about-us"
    }

    # 2. COMPETENCIA (Deep Linking para capturar textos de venta)
    COMPETITORS = [
        "https://www.ism.edu.ec/admisiones/",
        "https://www.jkepler.edu.ec/admisiones/",
        "https://www.einstein.k12.ec/admisiones/",
        "https://www.intisana.com/admisiones/",
        "https://colegioletort.edu.ec/admisiones/"
    ]
    
    # 3. CARGA DE INTELIGENCIA
    seeds = load_seeds("seeds.txt")
    if not seeds: return

    market = MarketData()
    all_keywords = market.get_suggestions(seeds)
    if not all_keywords: all_keywords = seeds

    scraper = SiteScraper("") # Instancia genérica
    
    # 4. AUDITORÍA INTERNA
    print(f"> FASE 1: Auditoría Interna ({len(TARGETS)} URLs)")
    site_corpus = {}
    for name, url in TARGETS.items():
        print(f"   Analizando: {name}")
        scraper.url = url
        data = scraper.audit()
        if data and data.get('content_sample'):
            site_corpus[name] = data['content_sample']

    if not site_corpus:
        print("   [FATAL] No hay datos internos.")
        return

    # 5. INTELIGENCIA COMPETITIVA
    print(f"\n> FASE 2: Benchmarking Competitivo")
    competitor_corpus = {}
    for url in COMPETITORS:
        scraper.url = url
        try:
            data = scraper.audit()
            if data and data.get('content_sample'):
                competitor_corpus[url] = data['content_sample']
                print(f"   Datos extraídos: {url}")
        except:
            print(f"   [!] Error en: {url}")

    # 6. PROCESAMIENTO ESTADÍSTICO
    print("\n> FASE 3: Cálculo Vectorial & Ponderación Comercial")
    analyzer = SEOAnalyzer(site_corpus, all_keywords)
    
    df_results = analyzer.run_matrix_analysis()
    
    comp_keywords_scored = []
    if competitor_corpus:
        comp_keywords_scored = analyzer.analyze_competitors(competitor_corpus)

    # 7. REPORTE FINAL
    print("\n> FASE 4: Generación de Entregable")
    if df_results is not None:
        reporter = StrategicReport()
        reporter.generate(
            df_results, 
            "output/heatmap_estrategico.png", 
            comp_keywords_scored, 
            COMPETITORS, 
            "output/Reporte_Ejecutivo_.pdf"
        )
    
    print("\n✅ PROCESO FINALIZADO. Revise la carpeta /output")

if __name__ == "__main__":
    main()