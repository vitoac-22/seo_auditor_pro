# UBICACIÓN: modules/analyzer.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os

class SEOAnalyzer:
    def __init__(self, site_corpus_dict, keywords):
        self.corpus = site_corpus_dict
        self.keywords = keywords
        
        # DICCIONARIO DE PESOS COMERCIALES (MARKETING BIAS)
        # Asignamos multiplicadores: 
        # 1.5x para dinero directo
        # 1.3x para urgencia/acción
        # 1.2x para calidad/autoridad
        self.commercial_weights = {
            'precio': 1.5, 'costo': 1.5, 'pension': 1.5, 'matricula': 1.5, 
            'inscripcion': 1.5, 'admision': 1.5, 'cupo': 1.5, '2026': 1.4,
            'abiertas': 1.3, 'requisitos': 1.3, 'agenda': 1.3, 'visita': 1.3,
            'contacto': 1.3, 'ubicacion': 1.2, 'norte': 1.2, 'quito': 1.1,
            'excelencia': 1.2, 'bilingue': 1.2, 'ingles': 1.2, 'tecnico': 1.2,
            'informatica': 1.2, 'seguridad': 1.2, 'bullying': 1.1
        }
        
        self.stop_words = [
            'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 
            'por', 'un', 'para', 'con', 'no', 'una', 'su', 'al', 'lo', 'como',
            'mas', 'pero', 'sus', 'le', 'ya', 'o', 'fue', 'este', 'ha', 'si', 
            'porque', 'esta', 'son', 'entre', 'muy', 'sin', 'sobre', 'ser',
            'tiene', 'tambien', 'me', 'hasta', 'hay', 'donde', 'quien', 'desde',
            'todo', 'nos', 'durante', 'todos', 'uno', 'les', 'ni', 'contra',
            'otros', 'ese', 'eso', 'ante', 'ellos', 'e', 'esto', 'mi', 'antes',
            'algunos', 'que', 'unos', 'yo', 'otro', 'otras', 'otra', 'el',
            'cual', 'poco', 'ella', 'estar', 'estos', 'algunas', 'algo',
            'nosotros', 'mi', 'mis', 'tu', 'tus', 'te', 'ti', 'web', 'sitio'
        ]

    def _get_weight(self, keyword):
        """Calcula el multiplicador comercial basado en palabras clave dentro de la frase."""
        weight = 1.0
        for trigger, multiplier in self.commercial_weights.items():
            if trigger in keyword.lower():
                # Si encuentra una palabra de dinero, aumenta el peso.
                # Usamos max para no multiplicar excesivamente si tiene muchas palabras.
                weight = max(weight, multiplier)
        return weight

    def analyze_competitors(self, competitor_corpus):
        """
        Analiza textos de la competencia y devuelve ranking ponderado.
        """
        print("      ... [IA] Analizando estrategia de competidores...")
        if not competitor_corpus: return []

        full_text = " ".join(competitor_corpus.values()).lower()
        
        try:
            vectorizer = TfidfVectorizer(stop_words=self.stop_words, max_features=300, ngram_range=(1,2))
            tfidf_matrix = vectorizer.fit_transform([full_text])
            feature_names = vectorizer.get_feature_names_out()
            scores = tfidf_matrix.toarray()[0]
            
            scored_keywords = []
            for word, score in zip(feature_names, scores):
                # Aplicamos sesgo comercial
                commercial_factor = self._get_weight(word)
                final_score = score * commercial_factor
                
                # Filtramos ruido y números puros
                if final_score > 0.05 and not word.replace('.','').isdigit():
                    scored_keywords.append((word, final_score))
            
            scored_keywords.sort(key=lambda x: x[1], reverse=True)
            return scored_keywords[:25]

        except ValueError:
            return []

    def run_matrix_analysis(self):
        print("      ... [IA] Calculando Matriz de Relevancia Cruzada (Weighted TF-IDF)")
        
        page_names = list(self.corpus.keys())
        page_texts = list(self.corpus.values())
        if not page_texts or not self.keywords: return None

        all_content = page_texts + self.keywords
        
        try:
            # ngram_range=(1,3) permite capturar frases como "colegio norte quito"
            vectorizer = TfidfVectorizer(stop_words=self.stop_words, ngram_range=(1,3))
            tfidf_matrix = vectorizer.fit_transform(all_content)
        except ValueError:
            print("      [Error] Contenido insuficiente para análisis vectorial.")
            return None

        page_vectors = tfidf_matrix[:len(page_names)]     
        keyword_vectors = tfidf_matrix[len(page_names):]  
        
        similarity_matrix = cosine_similarity(keyword_vectors, page_vectors)
        df_heatmap = pd.DataFrame(similarity_matrix, columns=page_names, index=self.keywords)
        
        if not os.path.exists('output'): os.makedirs('output')
        df_heatmap.to_csv("output/seo_matrix_raw.csv")

        # --- LÓGICA DE NEGOCIO: PONDERACIÓN ---
        # Calculamos un "Score de Oportunidad" que premia la intención transaccional
        df_heatmap['commercial_weight'] = [self._get_weight(k) for k in df_heatmap.index]
        
        # Max Value ponderado: (Mejor cobertura actual) * (Importancia comercial)
        # Esto nos ayuda a ordenar qué mostrar en el gráfico (lo más importante)
        df_heatmap['ranking_score'] = df_heatmap.drop(columns=['commercial_weight']).max(axis=1) * df_heatmap['commercial_weight']
        
        # Filtramos Top 40 por importancia comercial/estratégica
        df_top = df_heatmap.sort_values(by='ranking_score', ascending=False).head(40)
        
        # Limpiamos columnas auxiliares para el gráfico, pero mantenemos 'commercial_weight' para el reporte
        cols_to_plot = df_top.drop(columns=['ranking_score', 'commercial_weight'])
        
        self._generate_heatmap(cols_to_plot)
        
        # Retornamos el DF con la columna de peso para que el reporter sepa qué priorizar
        return df_top

    def _generate_heatmap(self, df):
        plt.figure(figsize=(14, 12))
        # cmap="RdYlGn" -> Rojo (0 coverage) a Verde (1 coverage). Más intuitivo para gerencia.
        sns.heatmap(df, annot=True, fmt=".2f", cmap="RdYlGn", cbar_kws={'label': 'Cobertura Actual (0=Riesgo, 1=Cubierto)'})
        plt.title('Matriz de Cobertura Estratégica: Demanda vs Oferta Actual')
        plt.xlabel('Páginas Auditadas')
        plt.ylabel('Intenciones de Búsqueda (Ordenadas por Valor Comercial)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('output/heatmap_estrategico.png')
        plt.close()