import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import numpy as np

class SEOAnalyzer:
    def __init__(self, site_corpus_dict, keywords, trend_data={}):
        self.corpus = site_corpus_dict
        self.keywords = keywords
        self.trend_data = trend_data # Diccionario {keyword: interest_score}
        
        self.stop_words = [
            'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 'por', 'un', 'para', 
            'con', 'no', 'una', 'su', 'al', 'lo', 'como', 'mas', 'pero', 'sus', 'le', 'ya', 'o', 
            'fue', 'este', 'ha', 'si', 'porque', 'esta', 'son', 'entre', 'muy', 'sin', 'sobre', 
            'ser', 'tiene', 'tambien', 'me', 'hasta', 'hay', 'donde', 'quien', 'desde', 'todo', 
            'nos', 'durante', 'todos', 'uno', 'les', 'ni', 'contra', 'otros', 'ese', 'eso', 'ante', 
            'ellos', 'e', 'esto', 'mi', 'antes', 'algunos', 'que', 'unos', 'yo', 'otro', 'otras', 
            'otra', 'el', 'cual', 'poco', 'ella', 'estar', 'estos', 'algunas', 'algo', 'nosotros', 
            'mi', 'mis', 'tu', 'tus', 'te', 'ti', 'web', 'sitio', 'pagina', 'inicio', 'menu', 
            'derechos', 'reservados', 'copyright', 'contactanos', 'telefono', 'email', 'direccion',
            'rey', 'sabio', 'salomon', 'unidad', 'educativa' # Stopwords de marca para ver gaps reales
        ]

    def classify_intent(self, keyword):
        kw = keyword.lower()
        if any(t in kw for t in ['precio', 'costo', 'pension', 'matricula', 'inscripcion', 'admision', 'cupo']):
            return "TRANSACCIONAL"
        if any(t in kw for t in ['mejor', 'ranking', 'top', 'comparativa', 'vs', 'lista']):
            return "COMERCIAL"
        return "INFORMACIONAL"

    def analyze_competitors(self, competitor_corpus):
        # (Mantén la lógica de competencia igual que antes, es sólida)
        # ... [copiar código anterior de analyze_competitors] ...
        # Si prefieres, te lo repito abajo completo.
        print("      ... [IA] Deconstruyendo competencia...")
        if not competitor_corpus: return []
        full_text = " ".join(competitor_corpus.values()).lower()
        try:
            vectorizer = TfidfVectorizer(stop_words=self.stop_words, max_features=500, ngram_range=(1,3))
            tfidf_matrix = vectorizer.fit_transform([full_text])
            feature_names = vectorizer.get_feature_names_out()
            scores = tfidf_matrix.toarray()[0]
            scored = []
            for w, s in zip(feature_names, scores):
                if s > 0.03 and len(w) > 3 and not w.isdigit():
                    scored.append((w, s, self.classify_intent(w)))
            scored.sort(key=lambda x: x[1], reverse=True)
            return scored[:40]
        except: return []

    def run_matrix_analysis(self):
        print("      ... [IA] Cruzando Cobertura vs Demanda Real (Trends)")
        
        page_names = list(self.corpus.keys())
        page_texts = list(self.corpus.values())
        if not page_texts or not self.keywords: return None

        all_content = page_texts + self.keywords
        
        try:
            vectorizer = TfidfVectorizer(stop_words=self.stop_words, ngram_range=(1,3))
            tfidf_matrix = vectorizer.fit_transform(all_content)
        except ValueError:
            return None

        page_vectors = tfidf_matrix[:len(page_names)]     
        keyword_vectors = tfidf_matrix[len(page_names):]  
        
        similarity_matrix = cosine_similarity(keyword_vectors, page_vectors)
        df = pd.DataFrame(similarity_matrix, columns=page_names, index=self.keywords)
        
        # --- AQUÍ ESTÁ LA MAGIA REAL ---
        # 1. Inyectamos el dato de Google Trends al DataFrame
        # Si la keyword no tiene dato (porque vino de suggest), le damos un valor bajo por defecto
        df['market_interest'] = [self.trend_data.get(k, 10) for k in df.index]
        
        # 2. Inyectamos la Intención
        df['intent'] = [self.classify_intent(k) for k in df.index]
        
        # 3. Calculamos la PRIORIDAD DE ACCIÓN (Action Priority Score)
        # Fórmula: (Interés de Mercado) * (1 - Cobertura Actual)
        # Si el interés es alto (100) y tu cobertura es baja (0.01), la Prioridad se dispara.
        df['max_coverage'] = df.drop(columns=['market_interest', 'intent']).max(axis=1)
        df['action_priority'] = df['market_interest'] * (1 - df['max_coverage'])
        
        # Ordenamos por Prioridad de Acción (Gaps Dolorosos primero)
        df_top = df.sort_values(by='action_priority', ascending=False).head(50)
        
        # Generar gráfico
        self._generate_heatmap(df_top.drop(columns=['market_interest', 'intent', 'max_coverage', 'action_priority']))
        
        return df_top

    def _generate_heatmap(self, df):
        plt.figure(figsize=(16, 14))
        sns.heatmap(df, annot=True, fmt=".2f", cmap="RdYlGn", cbar_kws={'label': 'Cobertura Semántica'})
        plt.title('Mapa de Calor: Oportunidades vs Contenido')
        plt.tight_layout()
        plt.savefig('output/heatmap_estrategico.png')
        plt.close()