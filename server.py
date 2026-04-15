"""
Custom static file server with clean URL routing.

Routes:
  /category/<slug>  →  category-dynamic.html?slug=<slug>
  /product/<slug>   →  product-<slug>.html  (if file exists)
                    →  product-dynamic.html?category=<slug>  (fallback)

Usage:
  python server.py          (default port 8000)
  python server.py 3000     (custom port)
"""

import sys
import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, urlencode

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)


class RoutingHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # Homepage: /index → /
        if path in ("/index", "/index.html"):
            self._redirect("/")
            return

        # /category/<slug>  →  /category-dynamic?slug=<slug>
        if path.startswith("/category/"):
            slug = path[len("/category/"):].strip("/")
            if slug:
                self._redirect(f"/category-dynamic?slug={slug}")
                return

        # /product/<slug>  →  static file if exists, else dynamic page
        if path.startswith("/product/"):
            slug = path[len("/product/"):].strip("/")
            if slug:
                static_file = f"product-{slug}.html"
                if os.path.exists(os.path.join(BASE_DIR, static_file)):
                    self._redirect(f"/product-{slug}")
                else:
                    self._redirect(f"/product-dynamic?category={slug}")
                return

        # Strip .html extension → redirect to clean URL (preserving query string)
        if path.endswith(".html"):
            clean = path[:-5]
            qs = parsed.query
            self._redirect(clean + ("?" + qs if qs else ""))
            return

        # Clean URL support: /page or /admin/page  →  serve page.html transparently
        last_segment = path.split("/")[-1]
        if last_segment and "." not in last_segment:
            candidate = path.lstrip("/") + ".html"
            if os.path.exists(os.path.join(BASE_DIR, candidate)):
                self.path = "/" + candidate
                super().do_GET()
                return

        super().do_GET()

    def _redirect(self, location):
        self.send_response(302)
        self.send_header("Location", location)
        self.end_headers()

    def log_message(self, fmt, *args):
        print(f"  {self.address_string()} — {fmt % args}")


if __name__ == "__main__":
    server = HTTPServer(("", PORT), RoutingHandler)
    print(f"Shining Horizon frontend running at http://localhost:{PORT}")
    print(f"  /category/<slug>  →  category-dynamic.html?slug=<slug>")
    print(f"  /product/<slug>   →  product-<slug>.html  (or dynamic fallback)")
    print("Press Ctrl+C to stop.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
