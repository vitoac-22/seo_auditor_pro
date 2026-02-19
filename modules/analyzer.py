import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

class SEOAnalyzer:
    def __init__(self, site_corpus_dict, keywords):
        self.corpus = site_corpus_dict
        self.keywords = keywords
        
        # Stop words estándar para limpieza lingüística
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

    def classify_intent(self, keyword):
        """
        Clasificación Categórica estándar en SEO (No inventada).
        Determina la etapa del funnel de ventas.
        """
        kw = keyword.lower()
        
        # 1. Transaccional (Do): El usuario quiere comprar/inscribirse YA.
        transactional_tokens = ['precio', 'costo', 'pension', 'matricula', 'inscripcion', 
                              'admision', 'cupo', 'comprar', 'valor', 'mensualidad', 'abiertas']
        if any(t in kw for t in transactional_tokens):
            return "TRANSACCIONAL"
            
        # 2. Comercial (Investigate): El usuario compara opciones.
        commercial_tokens = ['mejor', 'ranking', 'top', 'comparativa', 'vs', 'reseña', 
                           'opiniones', 'lista', 'norte', 'sur', 'quito', 'cumbaya']
        if any(t in kw for t in commercial_tokens):
            return "COMERCIAL"
            
        # 3. Informacional (Know): El usuario busca datos generales.
        informational_tokens = ['que', 'como', 'cuando', 'historia', 'metodologia', 
                              'educacion', 'significado', 'guia', 'consejos']
        if any(t in kw for t in informational_tokens):
            return "INFORMACIONAL"
            
        return "GENERICO" # Default

    def analyze_competitors(self, competitor_corpus):
        """
        Extrae las palabras más relevantes de la competencia usando TF-IDF puro.
        Esto revela qué palabras definen matemáticamente su contenido.
        """
        print("      ... [IA] Ejecutando extracción de entidades de competencia...")
        if not competitor_corpus: return []

        full_text = " ".join(competitor_corpus.values()).lower()
        
        try:
            # TF-IDF para detectar términos únicos y relevantes
            vectorizer = TfidfVectorizer(stop_words=self.stop_words, max_features=300, ngram_range=(1,2))
            tfidf_matrix = vectorizer.fit_transform([full_text])
            
            feature_names = vectorizer.get_feature_names_out()
            scores = tfidf_matrix.toarray()[0]
            
            # Mapeamos palabra -> puntaje real
            scored_keywords = []
            for word, score in zip(feature_names, scores):
                # Filtramos solo si tiene relevancia estadística real (>0.05)
                if score > 0.05 and not word.replace('.','').isdigit():
                    intent = self.classify_intent(word)
                    scored_keywords.append((word, score, intent))
            
            # Ordenamos por relevancia TF-IDF descendente
            scored_keywords.sort(key=lambda x: x[1], reverse=True)
            return scored_keywords[:30]

        except ValueError:
            return []

    def run_matrix_analysis(self):
        print("      ... [IA] Calculando Matriz Vectorial (Vector Space Model)")
        
        page_names = list(self.corpus.keys())
        page_texts = list(self.corpus.values())
        if not page_texts or not self.keywords: return None

        all_content = page_texts + self.keywords
        
        try:
            # Usamos n-gramas (1,3) para capturar frases compuestas
            vectorizer = TfidfVectorizer(stop_words=self.stop_words, ngram_range=(1,3))
            tfidf_matrix = vectorizer.fit_transform(all_content)
        except ValueError:
            print("      [Error] Corpus insuficiente para vectorización.")
            return None

        # Separamos vectores
        page_vectors = tfidf_matrix[:len(page_names)]     
        keyword_vectors = tfidf_matrix[len(page_names):]  
        
        # Cálculo de Similitud de Coseno (Métrica Estándar en NLP)
        similarity_matrix = cosine_similarity(keyword_vectors, page_vectors)
        
        # DataFrame con métricas puras
        df_heatmap = pd.DataFrame(similarity_matrix, columns=page_names, index=self.keywords)
        
        if not os.path.exists('output'): os.makedirs('output')
        
        # --- ENRIQUECIMIENTO DE DATOS ---
        # No alteramos el score, solo añadimos metadatos para el reporte
        df_heatmap['search_intent'] = [self.classify_intent(k) for k in df_heatmap.index]
        
        # Para el gráfico, usamos el máximo score de cobertura
        df_heatmap['max_coverage'] = df_heatmap.drop(columns=['search_intent']).max(axis=1)
        
        # Filtramos para visualización (Top 40 más relevantes o solicitadas)
        df_top = df_heatmap.sort_values(by='max_coverage', ascending=False).head(40)
        
        # Generamos el mapa de calor solo con datos numéricos
        cols_to_plot = df_top.drop(columns=['max_coverage', 'search_intent'])
        self._generate_heatmap(cols_to_plot)
        
        return df_top

    def _generate_heatmap(self, df):
        plt.figure(figsize=(14, 12))
        # RdYlGn: Rojo=0 (Sin cobertura), Verde=1 (Cobertura total)
        sns.heatmap(df, annot=True, fmt=".2f", cmap="RdYlGn", cbar_kws={'label': 'Similitud de Coseno (Relevancia Semántica)'})
        plt.title('Auditoría de Cobertura Semántica: Keywords vs URLs')
        plt.xlabel('Estructura Web Analizada')
        plt.ylabel('Keywords Objetivo')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('output/heatmap_estrategico.png')
        plt.close()