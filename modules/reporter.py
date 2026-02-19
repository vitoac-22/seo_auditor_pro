from fpdf import FPDF
import datetime
import os

class StrategicReport(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.page_width = 210 - 30 # A4 width - margins

    def sanitize(self, text):
        """Limpia caracteres para evitar errores de encoding en FPDF (Latin-1)."""
        if text is None: return ""
        text = str(text)
        try:
            return text.encode('latin-1', 'replace').decode('latin-1')
        except Exception:
            return text.encode('ascii', 'ignore').decode('ascii')

    def header(self):
        self.set_font('Arial', 'B', 9)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, self.sanitize('AUDITORÍA TÉCNICA DE CONTENIDOS | REY SABIO SALOMÓN'), 0, 0, 'R')
        self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Página {self.page_no()} - Generado por SEO Auditor Pro', 0, 0, 'C')

    def portada(self):
        self.add_page()
        self.set_y(80)
        
        # Título Impactante
        self.set_font('Arial', 'B', 26)
        self.set_text_color(15, 23, 42) # Azul oscuro corporativo
        self.cell(0, 20, self.sanitize("AUDITORÍA DE DENSIDAD SEMÁNTICA"), 0, 1, 'C')
        
        self.set_font('Arial', '', 14)
        self.set_text_color(100, 116, 139) # Gris azulado
        self.cell(0, 10, self.sanitize("Análisis de Brecha de Contenido y Oportunidades SEO"), 0, 1, 'C')
        
        self.ln(30)
        
        # Caja de Metadatos
        self.set_fill_color(241, 245, 249) # Gris muy claro
        self.rect(50, 140, 110, 40, 'F')
        self.set_y(145)
        
        self.set_font('Courier', '', 11)
        self.set_text_color(0, 0, 0)
        fecha = datetime.datetime.now().strftime("%d-%m-%Y")
        self.cell(0, 8, f"FECHA CORTE: {fecha}", 0, 1, 'C')
        self.cell(0, 8, self.sanitize("ALCANCE: Ecosistema Web Completo"), 0, 1, 'C')
        self.cell(0, 8, self.sanitize("ESTADO: REVISIÓN REQUERIDA"), 0, 1, 'C')

    def resumen_ejecutivo(self):
        self.add_page()
        self.set_font('Arial', 'B', 16)
        self.set_text_color(15, 23, 42)
        self.cell(0, 10, self.sanitize("1. Diagnóstico Ejecutivo"), 0, 1, 'L')
        self.ln(5)
        
        self.set_font('Arial', '', 11)
        self.set_text_color(51, 65, 85)
        texto = (
            "Este reporte analiza el contenido REAL de su sitio web, ignorando menús y pies de página "
            "para determinar la verdadera relevancia de cada URL.\n\n"
            "HALLAZGOS PRINCIPALES:\n"
            "1. Densidad de Palabras Clave: Se ha medido la frecuencia de términos estratégicos. "
            "Un score de 0.00 indica que la palabra no existe en el cuerpo del texto.\n"
            "2. Enfoque de Página: Cada URL debe atacar un grupo único de palabras. Si 'Básica' y 'Bachillerato' "
            "tienen los mismos scores, existe canibalización de contenido.\n"
            "3. Oportunidades: Las tablas a continuación muestran exactamente qué palabras inyectar en cada página "
            "para que Google entienda su temática específica."
        )
        self.multi_cell(0, 7, self.sanitize(texto))
        self.ln(10)

    def agregar_heatmap(self, image_path):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, self.sanitize("2. Matriz de Cobertura (Heatmap)"), 0, 1, 'L')
        self.ln(2)
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, self.sanitize("Visualización de la densidad de palabras clave por página."), 0, 1)
        self.ln(5)
        
        if os.path.exists(image_path):
            self.image(image_path, x=10, w=190)
        else:
            self.set_text_color(220, 38, 38)
            self.cell(0, 10, "[Error: Gráfico no generado]", 0, 1)
        self.ln(5)

    def seccion_competencia(self, competitor_data):
        self.add_page()
        self.set_font('Arial', 'B', 16)
        self.set_text_color(15, 23, 42)
        self.cell(0, 10, self.sanitize("3. Benchmarking de Competencia"), 0, 1, 'L')
        self.ln(5)
        
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 6, self.sanitize(
            "Análisis de los términos con mayor densidad en las webs de la competencia. "
            "Estos son los conceptos que ellos están posicionando agresivamente:"
        ))
        self.ln(5)

        # Cabecera de Tabla
        self.set_fill_color(30, 41, 59) # Azul oscuro
        self.set_text_color(255, 255, 255)
        self.set_font('Courier', 'B', 10)
        
        col_w = [70, 30, 40, 50] # Anchos de columna
        self.cell(col_w[0], 8, "TÉRMINO", 1, 0, 'L', 1)
        self.cell(col_w[1], 8, "SCORE", 1, 0, 'C', 1)
        self.cell(col_w[2], 8, "INTENCIÓN", 1, 0, 'C', 1)
        self.cell(col_w[3], 8, "ESTRATEGIA", 1, 1, 'L', 1)
        
        # Datos
        self.set_text_color(0, 0, 0)
        self.set_font('Courier', '', 9)
        
        if competitor_data:
            for i, (kw, score, intent) in enumerate(competitor_data[:20]): # Top 20
                bg = 255 if i % 2 == 0 else 245 # Filas alternas
                self.set_fill_color(bg, bg, bg)
                
                # Definir acción
                accion = "Blog / FAQ"
                if "TRANSACCIONAL" in intent: accion = "Landing Page"
                elif "COMERCIAL" in intent: accion = "Tabla Comparativa"
                
                self.cell(col_w[0], 7, self.sanitize(kw.upper()), 1, 0, 'L', 1)
                self.cell(col_w[1], 7, f"{score:.3f}", 1, 0, 'C', 1)
                self.cell(col_w[2], 7, self.sanitize(intent.split(' ')[0]), 1, 0, 'C', 1)
                self.cell(col_w[3], 7, self.sanitize(accion), 1, 1, 'L', 1)
        else:
            self.cell(0, 10, "No se obtuvieron datos suficientes de la competencia.", 1, 1)
            
        self.ln(10)

    def plan_accion(self, df_heatmap):
        self.add_page()
        self.set_font('Arial', 'B', 16)
        self.set_text_color(15, 23, 42)
        self.cell(0, 10, self.sanitize("4. Hoja de Ruta: Optimización On-Page"), 0, 1, 'L')
        self.ln(5)
        
        # Iterar páginas
        for pagina in df_heatmap.columns:
            if pagina in ['max_relevance', 'search_intent']: continue

            # Título de Página
            self.set_fill_color(71, 85, 105) # Slate grey
            self.set_text_color(255, 255, 255)
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, self.sanitize(f"  URL OBJETIVO: {pagina}  "), 0, 1, 'L', 1)
            self.ln(2)

            col_data = df_heatmap[pagina]
            
            # Clasificación de Keywords
            missing_critical = [] # No existen y son importantes
            low_density = []      # Existen pero muy poco
            optimized = []        # Están bien
            
            for kw, score in col_data.items():
                if score == 0.0:
                    missing_critical.append(kw)
                elif score < 0.05:
                    low_density.append(kw)
                else:
                    optimized.append((kw, score))
            
            # 1. CRÍTICO (Faltantes)
            if missing_critical:
                self.set_font('Arial', 'B', 10)
                self.set_text_color(185, 28, 28) # Rojo
                self.cell(0, 8, self.sanitize("  [!] CONTENIDO FALTANTE (Prioridad Alta):"), 0, 1)
                
                self.set_font('Courier', '', 10)
                self.set_text_color(0, 0, 0)
                # Mostrar en 2 columnas para ahorrar espacio
                chunks = [missing_critical[i:i + 2] for i in range(0, len(missing_critical), 2)]
                for chunk in chunks:
                    line = "   ".join([f"[ ] {kw.upper()}" for kw in chunk])
                    self.cell(0, 5, self.sanitize(line), 0, 1)
                self.ln(2)

            # 2. MEJORAS (Baja Densidad)
            if low_density:
                self.set_font('Arial', 'B', 10)
                self.set_text_color(194, 65, 12) # Naranja
                self.cell(0, 8, self.sanitize("  [+] AUMENTAR DENSIDAD (Mencionar más veces):"), 0, 1)
                self.set_font('Courier', '', 10)
                self.set_text_color(50, 50, 50)
                self.multi_cell(0, 5, self.sanitize(", ".join(low_density)))
                self.ln(2)

            # 3. OPTIMIZADO
            if optimized:
                self.set_font('Arial', 'B', 10)
                self.set_text_color(21, 128, 61) # Verde
                self.cell(0, 8, self.sanitize("  [OK] Términos bien posicionados:"), 0, 1)
                self.set_font('Courier', '', 9)
                self.set_text_color(100, 100, 100)
                top_3 = sorted(optimized, key=lambda x: x[1], reverse=True)[:5]
                text_opt = ", ".join([f"{kw} ({s:.2f})" for kw, s in top_3])
                self.multi_cell(0, 5, self.sanitize(text_opt))
            
            self.ln(8) # Espacio entre páginas

    def generate(self, df_results, chart_path, competitor_data, filename):
        self.portada()
        self.resumen_ejecutivo()
        self.agregar_heatmap(chart_path)
        if competitor_data:
            self.seccion_competencia(competitor_data)
        self.plan_accion(df_results)
        
        try:
            self.output(filename)
            print(f"   [Reporter] Reporte profesional generado: {filename}")
        except Exception as e:
            print(f"   [Reporter Error] {e}")