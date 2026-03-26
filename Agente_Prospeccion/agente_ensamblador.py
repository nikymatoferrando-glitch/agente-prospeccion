import csv
import os
import datetime

def empaquetar_leads_csv(nicho, ciudad, emails):
    """
    Órgano 4: Ensamblador de Producto Digital.
    Toma la recolección cruda del Scraper y la estandariza en un valioso archivo CSV B2B listo para su reventa.
    """
    print(f"\n[*] MOTOR 4 (Ensamblador): Empaquetando {len(emails)} correos purificados de '{nicho}' en '{ciudad}'...")
    
    if not emails:
        print("[-] Cero leads aptos extraídos. Abortando ensamblaje de producto.")
        return None
        
    # Limpiamos duplicados a un 'set' nuevamente por seguridad
    emails_unicos = list(set(emails))
        
    fecha = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    nicho_limpio = nicho.replace(' ', '_').lower()
    ciudad_limpia = ciudad.replace(' ', '_').lower()
    
    filename = f"producto_{nicho_limpio}_{ciudad_limpia}_{fecha}.csv"
    filepath = os.path.join(os.path.dirname(__file__), filename)
    
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Email', 'Nicho', 'Ciudad', 'Timestamp_Validacion_IA'])
            for em in emails_unicos:
                writer.writerow([em, nicho.title(), ciudad.title(), datetime.datetime.now().isoformat()])
                
        print(f"[+] EMPAQUETADO EXITOSO. Activo digital creado: {filepath}")
        return filepath
        
    except Exception as e:
        print(f"[!] ERROR al escribir el producto CSV: {e}")
        return None

if __name__ == '__main__':
    # Test
    empaquetar_leads_csv("odontologos", "buenos aires", ["clinica@test.com", "info@diente.com", "info@diente.com"])
