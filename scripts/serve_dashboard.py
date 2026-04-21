from __future__ import annotations

import http.server
import socketserver
import webbrowser
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PORT = 8000


def main() -> None:
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("127.0.0.1", PORT), handler) as httpd:
        print(f"CNT dashboard server root: {PROJECT_ROOT}")
        print(f"CNT dashboard URL: http://127.0.0.1:{PORT}/docs/cnt_operations_dashboard.html")
        try:
            webbrowser.open(f"http://127.0.0.1:{PORT}/docs/cnt_operations_dashboard.html")
        except Exception:
            pass
        httpd.serve_forever()


if __name__ == "__main__":
    import os

    os.chdir(PROJECT_ROOT)
    main()
