# UBICACIÓN: modules/scraper.py
import requests
from bs4 import BeautifulSoup
import warnings

# Ignoramos advertencias de SSL inseguro (común en webs institucionales)
warnings.filterwarnings("ignore")

class SiteScraper:
    def __init__(self, url):
        self.url = url
        # Nos disfrazamos de navegador legítimo
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        }

    def audit(self):
        print(f"   [Scraper] Conectando a {self.url}...")
        try:
            # verify=False es peligroso en producción bancaria, pero útil para scraping rápido
            response = requests.get(self.url, headers=self.headers, verify=False, timeout=10)
            
            if response.status_code != 200:
                print(f"   [Error] Status Code: {response.status_code}")
                return None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Limpieza básica de texto
            raw_text = soup.get_text(separator=' ', strip=True)
            
            data = {
                'title': soup.title.string if soup.title else "SIN TÍTULO",
                'h1': [h1.get_text(strip=True) for h1 in soup.find_all('h1')],
                'h2': [h2.get_text(strip=True) for h2 in soup.find_all('h2')],
                'meta_desc': "NO ENCONTRADA",
                'content_sample': raw_text[:10000], # Tomamos bastante contexto
                'word_count': len(raw_text.split())
            }
            
            meta = soup.find("meta", attrs={"name": "description"})
            if meta:
                data['meta_desc'] = meta.get("content")
                
            return data

        except Exception as e:
            print(f"   [Error Crítico] Falló el scraping: {e}")
            return None