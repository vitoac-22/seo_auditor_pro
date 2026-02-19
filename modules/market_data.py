import requests
import json
import time
import pandas as pd
from pytrends.request import TrendReq

class MarketData:
    def __init__(self):
        # Conectamos con Google Trends (hl='es-EC' para español de Ecuador)
        self.pytrends = TrendReq(hl='es-EC', tz=300)

    def get_real_trends(self, seeds):
        """
        Consulta el Índice de Interés (0-100) en Google Trends para las palabras clave.
        Retorna un diccionario {keyword: interest_score}.
        """
        print(f"   [Market] Consultando Google Trends para {len(seeds)} términos...")
        trend_scores = {}
        
        # Google Trends permite máximo 5 palabras por petición
        chunks = [seeds[i:i + 5] for i in range(0, len(seeds), 5)]
        
        for chunk in chunks:
            try:
                # Payload para Ecuador (geo='EC') y últimos 12 meses
                self.pytrends.build_payload(chunk, cat=0, timeframe='today 12-m', geo='EC')
                data = self.pytrends.interest_over_time()
                
                if not data.empty:
                    # Calculamos el promedio de interés anual
                    means = data.mean()
                    for kw, score in means.items():
                        trend_scores[kw] = round(score, 2)
                        print(f"      > {kw}: Interés {score:.1f}/100")
                
                # Pausa para no ser bloqueados por Google
                time.sleep(2) 
                
            except Exception as e:
                print(f"      [!] Error con Google Trends para {chunk}: {e}")
                # Fallback: Asignamos un score bajo por defecto si falla
                for kw in chunk:
                    trend_scores[kw] = 0

        return trend_scores

    def get_suggestions(self, seed_keywords):
        """
        Expande las semillas usando Autocomplete (Long tail keywords).
        """
        print(f"   [Market] Expandiendo lista con Google Suggest...")
        found_keywords = set(seed_keywords)
        base_url = "http://suggestqueries.google.com/complete/search?client=firefox&hl=es&gl=ec&q="
        
        for seed in seed_keywords:
            try:
                r = requests.get(base_url + seed.replace(' ', '+'), headers={'User-Agent': 'Mozilla/5.0'})
                if r.status_code == 200:
                    results = json.loads(r.text)[1]
                    for kw in results:
                        found_keywords.add(kw)
                time.sleep(0.2)
            except:
                continue
                
        return list(found_keywords)