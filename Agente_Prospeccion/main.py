import schedule
import time
import os
import sys

# Asegurar que el path esté correcto para las importaciones
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agente_prospeccion import run_pipeline_global

def job():
    print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Iniciando tarea autónoma de prospección DaaS...")
    try:
        run_pipeline_global()
    except Exception as e:
        print(f"[!] Error crítico durante la ejecución del job: {e}")

# Ejecutar todos los días a las 10:00 AM Hora local del servidor
schedule.every().day.at("10:00").do(job)

# También, programemos una ejecución cada 12 horas en caso de que un reinicio del server pierda el ciclo.
schedule.every(12).hours.do(job)

if __name__ == "__main__":
    print("================================================================")
    print("  INICIALIZANDO MOTOR PRINCIPAL DaaS (NUBE AUTÓNOMA)            ")
    print("================================================================")
    print("El worker ha arrancado exitosamente. Ejecutando primer ciclo de prueba...")
    
    # Ejecutamos una iteración inmediatamente al levantar el contenedor
    job()
    
    print("\n[+] Ciclo de arranque completado. Entrando en modo reposo de cron job.")
    
    # Bucle infinito del scheduler
    while True:
        schedule.run_pending()
        time.sleep(60) # Chequeo cada minuto
