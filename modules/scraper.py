import requests
from bs4 import BeautifulSoup
import warnings
import re

warnings.filterwarnings("ignore")

class SiteScraper:
    def __init__(self, url):
        self.url = url
        # Headers rotativos para parecer humano y evitar bloqueos de Google/Firewalls
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8'
        }

    def clean_text(self, text):
        """Limpia espacios dobles, tabulaciones y saltos de línea basura."""
        return re.sub(r'\s+', ' ', text).strip()

    def audit(self):
        print(f"   [Scraper] Conectando a {self.url}...")
        try:
            response = requests.get(self.url, headers=self.headers, verify=False, timeout=20)
            
            if response.status_code != 200:
                print(f"   [Error] Status Code: {response.status_code}")
                return None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # --- FASE 1: CIRUGÍA (Eliminación de Ruido) ---
            # Borramos menú, footer, sidebar, popups y scripts para que no contaminen el análisis
            noise_selectors = [
                'nav', 'footer', 'script', 'style', 'noscript', 'iframe', 'svg',
                '.navbar', '.menu', '.footer', '.sidebar', '#cookie-banner', 
                '.modal', '.popup', '#header', '.top-bar'
            ]
            for selector in noise_selectors:
                for element in soup.select(selector):
                    element.decompose() # Destruye el elemento del árbol HTML

            # --- FASE 2: EXTRACCIÓN INTELIGENTE ---
            # Buscamos el contenedor principal de Odoo o HTML5 estándar
            main_content = soup.find('main') or soup.find('div', id='wrap') or soup.find('div', class_='page-content') or soup.body
            
            if not main_content:
                main_content = soup

            # Extraemos texto limpio
            raw_text = main_content.get_text(separator=' ', strip=True)
            clean_body = self.clean_text(raw_text)

            # Debug: Mostrar qué texto único encontró (para que verifiques)
            print(f"      -> Texto único detectado: '{clean_body[:80]}...'")

            # --- FASE 3: METADATOS TÉCNICOS ---
            data = {
                'title': soup.title.string if soup.title else "SIN TÍTULO",
                'h1': [self.clean_text(h.get_text()) for h in soup.find_all('h1')],
                'h2': [self.clean_text(h.get_text()) for h in soup.find_all('h2')],
                'meta_desc': "NO ENCONTRADA",
                'content_sample': clean_body, # Aquí va el texto puro, sin menús
                'word_count': len(clean_body.split())
            }
            
            meta = soup.find("meta", attrs={"name": "description"})
            if meta:
                data['meta_desc'] = meta.get("content")
                
            return data

        except Exception as e:
            print(f"   [Error Crítico] Falló el scraping: {e}")
            return None