import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse

def find_emails_in_url(target_url, max_pages=3):
    """
    Órgano Cazador: Rastrea una URL localizando la información de contacto (Páginas amarillas, empresas, etc.)
    Avanza recursivamente por páginas de "Contacto" o "Nosotros" para atrapar los correos.
    """
    found_emails = set()
    visited_urls = set()
    urls_to_visit = [target_url]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print(f"[*] MOTOR 1 (Scraper): Iniciando rastreo silencioso en {target_url}...")

    while urls_to_visit and len(visited_urls) < max_pages:
        current_url = urls_to_visit.pop(0)
        
        if current_url in visited_urls:
            continue
            
        try:
            # Added verify=False because many local SMEs have expired/bad SSL certs
            response = requests.get(current_url, headers=headers, timeout=10, verify=False)
            visited_urls.add(current_url)
            
            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, 'html.parser')

            # 1. Búsqueda de fuerza bruta por Regex en todo el texto renderizado
            text_content = soup.get_text()
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text_content)
            
            # 2. Búsqueda semántica en hipervínculos
            for element in soup.find_all('a', href=True):
                href = element['href']
                if href.startswith('mailto:'):
                    email = href.replace('mailto:', '').split('?')[0].strip()
                    if email:
                        found_emails.add(email)
                
                # Aprovechar para enrutar el scraper sub-páginas clave (Contacto, About)
                if any(keyword in href.lower() for keyword in ['contacto', 'contact', 'about', 'nosotros', 'info']):
                    full_link = urljoin(target_url, href)
                    # No salir del dominio principal
                    if urlparse(full_link).netloc == urlparse(target_url).netloc:
                        if full_link not in visited_urls:
                            urls_to_visit.append(full_link)

            # 3. Filtrado de ruido
            for email in emails:
                if not email.endswith(('.png', '.jpg', '.jpeg', '.gif', '.css', '.js', '.webp')):
                    found_emails.add(email.lower())

        except Exception as e:
            print(f"[!] Error leyendo {current_url} - Objetivo Posiblemente Caído: {e}")

    return list(found_emails)

if __name__ == '__main__':
    # EJECUCIÓN DE PRUEBA LOCAL
    # Prueba con la URL de alguna PYME local o empresa a la que quieras venderle
    test_url = "https://www.google.com" # Cambiar por una empresa B2B real para probar
    correos = find_emails_in_url(test_url, max_pages=3)
    print(f"\n[+] Resultados Finales: {len(correos)} correos extraídos -> {correos}")
