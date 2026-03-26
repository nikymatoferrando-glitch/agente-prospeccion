import schedule
import time
import os
import sys
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# Ensure path is correct for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agente_prospeccion import run_pipeline_global

class HealthCheckHandler(BaseHTTPRequestHandler):
        def do_GET(self):
                    self.send_response(200)
                    self.send_header('Content-type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(b"OK")

        def log_message(self, format, *args):
                    return # Silence logs

def run_health_check_server():
        port = int(os.environ.get("PORT", 10000))
        print(f"[*] Health server active on port {port}")
        httpd = HTTPServer(('', port), HealthCheckHandler)
        httpd.serve_forever()

def job():
        print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting autonomous prospecting task...")
        try:
                    run_pipeline_global()
except Exception as e:
        print(f"[!] Critical error during job: {e}")

# Run every day at 10:00 AM server time
schedule.every().day.at("10:00").do(job)

# Also run every 12 hours
schedule.every(12).hours.do(job)

if __name__ == "__main__":
        # Start health server for Render
        threading.Thread(target=run_health_check_server, daemon=True).start()

    print("================================================================")
    print("  INITIALIZING MOTOR PRINCIPAL DaaS (AUTONOMOUS CLOUD)          ")
    print("================================================================")
    print("Worker started successfully. Running first test cycle...")

    # Run one iteration immediately
    job()

    print("\n[+] Startup cycle completed. Entering cron job mode.")

    # scheduler loop
    while True:
                schedule.run_pending()
                time.sleep(60)
        
