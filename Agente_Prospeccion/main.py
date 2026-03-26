import schedule
import time
import os
import sys
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agente_prospeccion import run_pipeline_global

class HealthCheckHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/plain')
    self.end_headers()
    self.wfile.write(b"OK")
    def log_message(self, *args): pass

    def run_health_check_server():
      port = int(os.environ.get("PORT", 10000))
      httpd = HTTPServer(('', port), HealthCheckHandler)
      httpd.serve_forever()

def job():
  print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Iniciando tarea...")
  try:
    run_pipeline_global()
  except Exception as e:
    print(f"Error: {e}")

schedule.every().day.at('10:00').do(job)
schedule.every(12).hours.do(job)

if __name__ == '__main__':
  threading.Thread(target=run_health_check_server, daemon=True).start()
  job()
  while True:
    schedule.run_pending()
    time.sleep(60)
    
