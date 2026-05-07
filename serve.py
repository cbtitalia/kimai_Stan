#!/usr/bin/env python3
"""
Serveur HTTP simple pour le dashboard
"""

import http.server
import socketserver
import os
from pathlib import Path

PORT = 8000
DASHBOARD_DIR = Path(__file__).parent / ".." / "wiki" / "Informatique" / "Pointage_Stan"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DASHBOARD_DIR), **kwargs)

    def log_message(self, format, *args):
        print(f"📡 {format % args}")

if __name__ == "__main__":
    os.chdir(DASHBOARD_DIR)

    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"""
╔════════════════════════════════════════════╗
║   🎨 Dashboard Kimai - Serveur HTTP         ║
╚════════════════════════════════════════════╝

📍 Ouvre dans ton navigateur:
   http://localhost:{PORT}/dashboard.html

📊 Dossier servi: {DASHBOARD_DIR}

⏸️  Appuie sur Ctrl+C pour arrêter

═════════════════════════════════════════════
""")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✅ Serveur arrêté")
