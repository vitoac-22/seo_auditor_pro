# UBICACIÓN: modules/reporter.py
from fpdf import FPDF
import datetime
import os

class StrategicReport(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)

    def sanitize(self, text):
        if text is None: return ""
        text = str(text)
        try:
            return text.encode('latin-1', 'replace').decode('latin-1')
        except Exception:
            return text.encode('ascii', 'ignore').decode('ascii')

    def header(self):
        self.set_font('Arial', 'B', 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, self.sanitize('CONFIDENCIAL | Auditoría de Inteligencia de Mercado'), 0, 0, 'R')
        self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Pagina {self.page_no()} - Generado por Python SEO Auditor Pro', 0, 0, 'C')

    def portada(self):
        self.add_page()
        self.set_fill_color(30, 30, 30) # Fondo oscuro
        self.rect(0, 0, 210, 297, 'F') # Página negra para impacto
        
        self.set_y(80)
        self.set_font('Arial', 'B', 28)
        self.set_text_color(255, 255, 255)
        self.cell(0, 20, self.sanitize("AUDITORÍA DE ECOSISTEMA DIGITAL"), 0, 1, 'C')
        
        self.set_font('Arial', '', 16)
        self.set_text_color(200, 200, 200)
        self.cell(0, 10, self.sanitize("Análisis de Brecha Semántica & Competencia"), 0, 1, 'C')
        self.ln(20)
        
        self.set_font('Courier', 'B', 12)
        self.set_text_color(0, 255, 0) # Verde terminal
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self.cell(0, 8, f"> TARGET: Unidad Educativa Rey Sabio Salomon", 0, 1, 'C')
        self.cell(0, 8, f"> FECHA: {fecha}", 0, 1, 'C')
        self.cell(0, 8, f"> ESTADO: ANALISIS CRITICO FINALIZADO", 0, 1, 'C')

    def resumen_ejecutivo(self):
        self.add_page()
        self.set_text_color(0, 0, 0)
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, self.sanitize("1. Resumen Ejecutivo (Executive Summary)"), 0, 1, 'L')
        self.ln(5)
        
        self.set_font('Arial', '', 11)
        texto = (
            "Hemos sometido su sitio web a un análisis vectorial contra sus competidores directos. "
            "Los datos revelan una asimetría crítica: mientras su competencia optimiza para CONVERSIÓN "
            "(palabras transaccionales como 'Inscripciones', 'Costos'), su sitio actual optimiza "
            "mayormente para DESCRIPCIÓN INSTITUCIONAL.\n\n"
            "HALLAZGOS CLAVE:\n"
            "1. Riesgo de Invisibilidad: Palabras clave de alto valor como 'Bachillerato Técnico' tienen "
            "una cobertura cercana a cero en sus páginas principales.\n"
            "2. Oportunidad Estadística: Existe un 'Océano Azul' en el nicho de 'Seguridad + Norte de Quito' "
            "que la competencia está descuidando.\n"
            "3. Acción Recomendada: Ejecutar las inyecciones de contenido listadas en la Sección 4 "
            "para corregir la entropía semántica inmediatamente."
        )
        self.multi_cell(0, 7, self.sanitize(texto))
        self.ln(10)

    def agregar_grafica(self, image_path):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, self.sanitize("2. Matriz de Cobertura (Visualización del Riesgo)"), 0, 1, 'L')
        self.ln(2)
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, self.sanitize("Rojo = Zona de Riesgo (Vacío) | Verde = Zona Segura"), 0, 1)
        
        if os.path.exists(image_path):
            self.image(image_path, x=10, w=190)
        else:
            self.cell(0, 10, "Gráfico no disponible", 0, 1)
        self.ln(5)

    def seccion_competencia(self, competitor_data, competitor_urls):
        self.add_page()
        self.set_font('Arial', 'B', 16)
        self.set_text_color(180, 0, 0)
        self.cell(0, 10, self.sanitize("3. Benchmarking Competitivo"), 0, 1, 'L')
        self.ln(5)
        
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 6, self.sanitize(
            "Se han analizado los siguientes dominios rivales para extraer sus palabras de mayor tracción:"
        ))
        self.set_font('Courier', '', 9)
        for url in competitor_urls:
            clean = url.replace('https://','').split('/')[0]
            self.cell(0, 5, self.sanitize(f"  - {clean}"), 0, 1)
        self.ln(5)
        
        self.set_font('Arial', 'B', 11)
        self.cell(0, 10, self.sanitize("Top Keywords Transaccionales de la Competencia:"), 0, 1)
        
        # Tabla estilo terminal
        self.set_fill_color(240, 240, 240)
        self.set_font('Courier', 'B', 10)
        self.cell(80, 8, "KEYWORD", 1, 0, 'L', 1)
        self.cell(40, 8, "INTENSIDAD", 1, 0, 'C', 1)
        self.cell(70, 8, "TIPO DETECTADO", 1, 1, 'L', 1)
        
        self.set_font('Courier', '', 10)
        if competitor_data:
            for kw, score in competitor_data:
                # Calculamos tipo basado en triggers
                tipo = "GENERICO"
                if any(x in kw for x in ['precio', 'costo', 'pension', 'matricula']): tipo = "DINERO ($$$)"
                elif any(x in kw for x in ['ingles', 'bilingue', 'cambridge']): tipo = "ACADEMICO"
                elif any(x in kw for x in ['admision', 'inscripcion', 'cupo']): tipo = "ACCION"
                
                self.cell(80, 7, self.sanitize(kw.upper()), 1)
                self.cell(40, 7, f"{score:.3f}", 1, 0, 'C')
                self.cell(70, 7, tipo, 1, 1)
        self.ln(10)

    def plan_accion(self, df_heatmap):
        self.add_page()
        self.set_text_color(0, 0, 0)
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, self.sanitize("4. Plan de Mitigación por URL (Actionable Insights)"), 0, 1, 'L')
        self.ln(5)
        
        for pagina in df_heatmap.columns:
            if pagina in ['ranking_score', 'commercial_weight']: continue

            self.set_fill_color(0, 51, 102)
            self.set_text_color(255, 255, 255)
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, self.sanitize(f"  URL OBJETIVO: {pagina}  "), 0, 1, 'L', 1)
            self.set_text_color(0, 0, 0)
            self.ln(2)

            col_data = df_heatmap[pagina]
            weights = df_heatmap['commercial_weight']
            
            # Cruzamos data con peso comercial
            # Queremos ver GAPS (score bajo) pero con PESO ALTO
            gaps = []
            strengths = []
            
            for kw, score in col_data.items():
                weight = weights[kw]
                if score < 0.1: # Es un vacío
                    # Prioridad = Peso comercial
                    gaps.append((kw, weight))
                elif score > 0.2:
                    strengths.append((kw, score))
            
            # Ordenamos GAPS por peso comercial (Lo más urgente primero)
            gaps.sort(key=lambda x: x[1], reverse=True)
            strengths.sort(key=lambda x: x[1], reverse=True)

            # Renderizamos Gaps
            self.set_font('Arial', 'B', 10)
            self.set_text_color(200, 0, 0)
            self.cell(0, 8, self.sanitize("  [!] OPORTUNIDADES CRÍTICAS (Inyectar texto aquí):"), 0, 1)
            
            self.set_font('Courier', '', 10)
            self.set_text_color(0, 0, 0)
            if gaps:
                for kw, w in gaps[:8]: # Top 8 urgencias
                    urgencia = "ALTA" if w > 1.3 else "MEDIA"
                    self.cell(0, 5, self.sanitize(f"    [ ] {kw.upper()} (Prioridad: {urgencia})"), 0, 1)
            else:
                self.cell(0, 5, "    (Sin vacíos críticos detectados)", 0, 1)
            
            self.ln(2)
            # Renderizamos Fortalezas
            self.set_font('Arial', 'B', 10)
            self.set_text_color(0, 100, 0)
            self.cell(0, 8, self.sanitize("  [OK] FORTALEZAS (No tocar):"), 0, 1)
            self.set_font('Courier', '', 9)
            self.set_text_color(100, 100, 100)
            if strengths:
                for kw, s in strengths[:3]:
                    self.cell(0, 5, self.sanitize(f"    - {kw}"), 0, 1)
            
            self.ln(8)

    def generate(self, df_results, chart_path, competitor_data, competitor_urls, filename="output/Reporte_Ejecutivo_SEO.pdf"):
        self.portada()
        self.resumen_ejecutivo()
        self.agregar_grafica(chart_path)
        if competitor_data:
            self.seccion_competencia(competitor_data, competitor_urls)
        self.plan_accion(df_results)
        
        try:
            self.output(filename)
            print(f"   [Reporter] PDF generado: {filename}")
        except Exception as e:
            print(f"   [Reporter Error] {e}")