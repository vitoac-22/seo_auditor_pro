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
        self.cell(0, 10, self.sanitize('AUDITORÍA TÉCNICA SEO | REY SABIO SALOMÓN'), 0, 0, 'R')
        self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')

    def portada(self):
        self.add_page()
        self.set_y(80)
        self.set_font('Arial', 'B', 24)
        self.set_text_color(0, 0, 0)
        self.cell(0, 20, self.sanitize("INFORME DE RENDIMIENTO SEMÁNTICO"), 0, 1, 'C')
        
        self.set_font('Arial', '', 14)
        self.set_text_color(80, 80, 80)
        self.cell(0, 10, self.sanitize("Análisis Vectorial de Contenido y Competencia"), 0, 1, 'C')
        self.ln(20)
        
        self.set_font('Courier', '', 11)
        self.set_text_color(0, 0, 0)
        fecha = datetime.datetime.now().strftime("%Y-%m-%d")
        self.cell(0, 8, f"Fecha de Corte: {fecha}", 0, 1, 'C')
        self.cell(0, 8, self.sanitize("Metodología: TF-IDF & Cosine Similarity"), 0, 1, 'C')

    def resumen_tecnico(self):
        self.add_page()
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, self.sanitize("1. Resumen Técnico"), 0, 1, 'L')
        self.ln(5)
        
        self.set_font('Arial', '', 11)
        texto = (
            "Este reporte utiliza métricas de Recuperación de Información (IR) para medir la distancia "
            "semántica entre su contenido actual y las consultas de búsqueda del mercado.\n\n"
            "DEFINICIONES:\n"
            "- Cobertura (0.0 - 1.0): Nivel de similitud matemática. 1.0 es una coincidencia exacta.\n"
            "- Gap Semántico: Términos con cobertura < 0.1 (El motor de búsqueda no ve relevancia).\n"
            "- Intención Transaccional: Palabras clave que denotan una acción de conversión inmediata.\n\n"
            "DIAGNÓSTICO GENERAL:\n"
            "Se ha detectado una desconexión entre el vocabulario institucional (Misión, Visión) y "
            "el vocabulario de mercado (Precios, Inscripciones, Ubicación)."
        )
        self.multi_cell(0, 7, self.sanitize(texto))
        self.ln(10)

    def agregar_heatmap(self, image_path):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, self.sanitize("2. Matriz de Cobertura Semántica"), 0, 1, 'L')
        self.ln(5)
        if os.path.exists(image_path):
            self.image(image_path, x=10, w=190)
        else:
            self.cell(0, 10, "Gráfico no disponible", 0, 1)
        self.ln(5)

    def seccion_competencia(self, competitor_data, competitor_urls):
        self.add_page()
        self.set_font('Arial', 'B', 16)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, self.sanitize("3. Análisis Vectorial de Competencia"), 0, 1, 'L')
        self.ln(5)
        
        self.set_font('Arial', '', 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 6, self.sanitize("Términos con mayor peso TF-IDF en los sitios web de la competencia:"))
        self.ln(5)

        # Tabla
        self.set_fill_color(240, 240, 240)
        self.set_font('Courier', 'B', 10)
        self.cell(80, 8, "TÉRMINO (TOKEN)", 1, 0, 'L', 1)
        self.cell(40, 8, "RELEVANCIA", 1, 0, 'C', 1)
        self.cell(70, 8, "CLASIFICACIÓN", 1, 1, 'L', 1)
        
        self.set_font('Courier', '', 10)
        if competitor_data:
            for kw, score, intent in competitor_data:
                self.cell(80, 7, self.sanitize(kw.upper()), 1)
                self.cell(40, 7, f"{score:.4f}", 1, 0, 'C') # 4 decimales = precisión científica
                self.cell(70, 7, self.sanitize(intent), 1, 1)
        self.ln(10)

    def plan_accion(self, df_heatmap):
        self.add_page()
        self.set_font('Arial', 'B', 16)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, self.sanitize("4. Plan de Optimización (Gap Analysis)"), 0, 1, 'L')
        self.ln(5)
        
        for pagina in df_heatmap.columns:
            if pagina in ['max_coverage', 'search_intent']: continue

            self.set_fill_color(50, 50, 50)
            self.set_text_color(255, 255, 255)
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, self.sanitize(f"  PÁGINA: {pagina}  "), 0, 1, 'L', 1)
            self.set_text_color(0, 0, 0)
            self.ln(2)

            col_data = df_heatmap[pagina]
            intents = df_heatmap['search_intent']
            
            # Clasificación lógica de tareas
            critical_gaps = [] # Transaccionales faltantes
            opportunity_gaps = [] # Comerciales faltantes
            
            for kw, score in col_data.items():
                intent = intents[kw]
                if score < 0.1: # GAP DETECTADO
                    if intent == "TRANSACCIONAL":
                        critical_gaps.append(kw)
                    elif intent == "COMERCIAL":
                        opportunity_gaps.append(kw)
            
            # Renderizado Priorizado
            self.set_font('Arial', 'B', 10)
            self.set_text_color(200, 0, 0)
            if critical_gaps:
                self.cell(0, 8, self.sanitize("  [!] PRIORIDAD ALTA (Transaccional - Faltante):"), 0, 1)
                self.set_font('Courier', '', 10)
                self.set_text_color(0, 0, 0)
                for kw in critical_gaps:
                    self.cell(0, 5, self.sanitize(f"    [ ] {kw.upper()}"), 0, 1)
            else:
                self.set_text_color(0, 100, 0)
                self.cell(0, 8, self.sanitize("  [OK] Cobertura Transaccional Adecuada"), 0, 1)
            
            self.ln(2)
            if opportunity_gaps:
                self.set_font('Arial', 'B', 10)
                self.set_text_color(255, 140, 0) # Naranja
                self.cell(0, 8, self.sanitize("  [i] OPORTUNIDADES DE POSICIONAMIENTO (Comercial):"), 0, 1)
                self.set_font('Courier', '', 10)
                self.set_text_color(0, 0, 0)
                for kw in opportunity_gaps:
                    self.cell(0, 5, self.sanitize(f"    - {kw}"), 0, 1)
            
            self.ln(8)

    def generate(self, df_results, chart_path, competitor_data, competitor_urls, filename):
        self.portada()
        self.resumen_tecnico()
        self.agregar_heatmap(chart_path)
        if competitor_data:
            self.seccion_competencia(competitor_data, competitor_urls)
        self.plan_accion(df_results)
        
        try:
            self.output(filename)
            print(f"   [Reporter] PDF generado: {filename}")
        except Exception as e:
            print(f"   [Reporter Error] {e}")