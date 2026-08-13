#!/usr/bin/env python3
"""Serves the registry on port 80 so a made-up domain in /etc/hosts resolves to it.

    sudo python3 site/serve.py

Pair with an /etc/hosts line pointing your chosen name at 127.0.0.1. Use a name you
have confirmed is unregistered, or a .test name, which is reserved and can never
resolve publicly. Plain HTTP only: do not use .dev or .app, which browsers force to
HTTPS. Nothing here impersonates a real site.
"""
import functools, http.server, pathlib, socketserver

ROOT = pathlib.Path(__file__).parent
PORT = 80

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("127.0.0.1", PORT), handler) as httpd:
    print(f"Registry served from {ROOT} on http://127.0.0.1:{PORT}")
    print("Stop with Ctrl+C.")
    httpd.serve_forever()
