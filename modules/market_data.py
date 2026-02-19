# UBICACIÓN: modules/market_data.py
import requests
import json
import time

class MarketData:
    def get_suggestions(self, seed_keywords):
        print(f"   [Market] Buscando sugerencias para {len(seed_keywords)} semillas...")
        found_keywords = set(seed_keywords)
        
        # API de autocompletado de Google (Configurada para Español - hl=es)
        base_url = "http://suggestqueries.google.com/complete/search?client=firefox&hl=es&gl=ec&q="
        
        for seed in seed_keywords:
            try:
                # Limpiamos espacios para la URL
                query = seed.replace(' ', '+')
                r = requests.get(base_url + query, headers={'User-Agent': 'Mozilla/5.0'})
                
                if r.status_code == 200:
                    results = json.loads(r.text)[1]
                    for kw in results:
                        found_keywords.add(kw)
                    # Pausa ética para no ser baneados por Google
                    time.sleep(0.5)
            except Exception as e:
                print(f"   [Alerta] Error buscando '{seed}': {e}")
                continue
                
        print(f"   [Market] Total keywords encontradas: {len(found_keywords)}")
        return list(found_keywords)