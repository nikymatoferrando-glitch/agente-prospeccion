import schedule
import time
import os
import sys
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# Asegurar que el path este correcto para las importaciones
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agente_prospeccion import run_pipeline_global

class HealthCheckHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/plain')
    self.end_headers()
    self.wfile.write(b"OK")
    def log_message(self, format, *args):
      return

def run_health_check_server():
  port = int(os.environ.get("PORT", 10000))
  print(f"[*] Servidor de salud activo en puerto {port}")
  httpd = HTTPServer(('', port), HealthCheckHandler)
  httpd.serve_forever()

def job():
  print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Iniciando tarea autonoma de prospeccion DaaS...")
  try:
    run_pipeline_global()
  except Exception as e:
    print(f"[!] Error critico durante la ejecucion del job: {e}")

# Programar tareas
schedule.every().day.at('10:00').do(job)
schedule.every(12).hours.do(job)

if __name__ == '__main__':
  threading.Thread(target=run_health_check_server, daemon=True).start()
  print('INICIALIZANDO MOTOR PRINCIPAL')
  job()
  while True:
    schedule.run_pending()
    time.sleep(60)
    
