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
        self.cell(0, 20, self.sanitize("INFORME DE ESTRATEGIA DE POSICIONAMIENTO"), 0, 1, 'C')
        
        self.set_font('Arial', '', 14)
        self.set_text_color(80, 80, 80)
        self.cell(0, 10, self.sanitize("Análisis de Brecha Semántica vs Competencia (Benchmarking)"), 0, 1, 'C')
        self.ln(20)
        
        self.set_font('Courier', '', 11)
        self.set_text_color(0, 0, 0)
        fecha = datetime.datetime.now().strftime("%Y-%m-%d")
        self.cell(0, 8, f"Fecha de Corte: {fecha}", 0, 1, 'C')
        self.cell(0, 8, self.sanitize("Metodología: TF-IDF (Relevancia Real) & Clasificación de Intención"), 0, 1, 'C')

    def resumen_tecnico(self):
        self.add_page()
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, self.sanitize("1. Guía de Interpretación de Datos"), 0, 1, 'L')
        self.ln(5)
        
        self.set_font('Arial', '', 11)
        texto = (
            "Para tomar decisiones basadas en este reporte, entienda los siguientes indicadores:\n\n"
            "1. RELEVANCIA (Score 0.0 - 1.0):\n"
            "   Indica qué tan importante es una palabra para Google. Un score alto en la competencia "
            "significa que ellos basan su estrategia en ese término.\n\n"
            "2. INTENCIÓN DE BÚSQUEDA (El 'Por qué'):\n"
            "   - TRANSACCIONAL ($): El usuario quiere inscribirse o saber precios. (USAR EN BOTONES/TÍTULOS)\n"
            "   - COMERCIAL (?): El usuario compara colegios ('Mejores', 'Ranking'). (USAR EN BLOGS)\n"
            "   - INFORMACIONAL (i): El usuario busca datos generales. (USAR EN PÁRRAFOS)\n\n"
            "3. GAP (Brecha):\n"
            "   Es una palabra que la competencia usa intensivamente y su sitio web ignora por completo."
        )
        self.multi_cell(0, 7, self.sanitize(texto))
        self.ln(10)

    def agregar_heatmap(self, image_path):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, self.sanitize("2. Matriz Visual de Cobertura"), 0, 1, 'L')
        self.ln(2)
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, self.sanitize("Rojo = Oportunidad Perdida (Nadie lo usa) | Verde = Territorio Ganado"), 0, 1)
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
        self.cell(0, 10, self.sanitize("3. Radiografía de la Competencia"), 0, 1, 'L')
        self.ln(5)
        
        self.set_font('Arial', '', 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 6, self.sanitize(
            "Se analizaron las páginas de Admisiones/Oferta de los siguientes colegios para extraer su vocabulario de venta:"
        ))
        
        self.set_font('Courier', '', 9)
        for url in competitor_urls:
            clean = url.replace('https://','').replace('www.','').split('/')[0]
            self.cell(0, 5, self.sanitize(f"  - {clean}"), 0, 1)
        self.ln(5)

        self.set_font('Arial', 'B', 11)
        self.cell(0, 10, self.sanitize("Top Términos que la Competencia usa para Vender:"), 0, 1)

        # Encabezados de Tabla
        self.set_fill_color(230, 230, 230)
        self.set_font('Courier', 'B', 9)
        self.cell(60, 8, "TÉRMINO DETECTADO", 1, 0, 'L', 1)
        self.cell(30, 8, "INTENSIDAD", 1, 0, 'C', 1)
        self.cell(40, 8, "TIPO", 1, 0, 'C', 1)
        self.cell(60, 8, "ACCIÓN SUGERIDA", 1, 1, 'L', 1)
        
        self.set_font('Courier', '', 9)
        if competitor_data:
            for kw, score, intent in competitor_data:
                # Definir acción sugerida basada en lógica real
                accion = "Crear contenido educativo"
                if intent == "TRANSACCIONAL":
                    accion = "USAR EN H1 / BOTÓN CTA"
                    self.set_text_color(0, 100, 0) # Verde para dinero
                elif intent == "COMERCIAL":
                    accion = "Crear Tabla Comparativa"
                    self.set_text_color(200, 100, 0) # Naranja
                else:
                    self.set_text_color(0, 0, 0)

                self.cell(60, 7, self.sanitize(kw.upper()), 1)
                self.cell(30, 7, f"{score:.4f}", 1, 0, 'C')
                self.cell(40, 7, self.sanitize(intent), 1, 0, 'C')
                self.cell(60, 7, self.sanitize(accion), 1, 1)
                self.set_text_color(0, 0, 0) # Reset
        self.ln(10)

    def plan_accion(self, df_heatmap):
        self.add_page()
        self.set_font('Arial', 'B', 16)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, self.sanitize("4. Hoja de Ruta (Qué usar y dónde)"), 0, 1, 'L')
        self.ln(5)
        
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 6, self.sanitize(
            "A continuación se listan las Oportunidades Reales. Estas son palabras que tienen alta demanda "
            "pero que su página web actual NO está utilizando (Cobertura Baja)."
        ))
        self.ln(5)

        for pagina in df_heatmap.columns:
            if pagina in ['max_coverage', 'search_intent']: continue

            self.set_fill_color(0, 51, 102)
            self.set_text_color(255, 255, 255)
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, self.sanitize(f"  PÁGINA OBJETIVO: {pagina}  "), 0, 1, 'L', 1)
            self.set_text_color(0, 0, 0)
            self.ln(2)

            col_data = df_heatmap[pagina]
            intents = df_heatmap['search_intent']
            
            # Clasificación lógica de tareas
            critical_gaps = [] 
            opportunity_gaps = [] 
            
            for kw, score in col_data.items():
                intent = intents[kw]
                if score < 0.1: # GAP REAL (No usado)
                    if intent == "TRANSACCIONAL":
                        critical_gaps.append(kw)
                    elif intent == "COMERCIAL":
                        opportunity_gaps.append(kw)
            
            # Renderizado Priorizado
            if critical_gaps:
                self.set_font('Arial', 'B', 10)
                self.set_text_color(200, 0, 0)
                self.cell(0, 8, self.sanitize("  [!] DEBES USAR ESTO (Conversión Directa):"), 0, 1)
                self.set_font('Courier', '', 10)
                self.set_text_color(0, 0, 0)
                for kw in critical_gaps:
                    self.cell(0, 5, self.sanitize(f"    [ ] {kw.upper()} -> Añadir en Título o Primer Párrafo"), 0, 1)
                self.ln(3)

            if opportunity_gaps:
                self.set_font('Arial', 'B', 10)
                self.set_text_color(255, 140, 0) # Naranja
                self.cell(0, 8, self.sanitize("  [i] OPORTUNIDADES DE TRÁFICO (Comparación):"), 0, 1)
                self.set_font('Courier', '', 10)
                self.set_text_color(0, 0, 0)
                for kw in opportunity_gaps:
                    self.cell(0, 5, self.sanitize(f"    - {kw} -> Crear artículo de blog o sección FAQ"), 0, 1)
            
            if not critical_gaps and not opportunity_gaps:
                 self.set_font('Arial', 'I', 10)
                 self.set_text_color(0, 100, 0)
                 self.cell(0, 8, self.sanitize("  [OK] Esta página está bien optimizada para las palabras analizadas."), 0, 1)

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