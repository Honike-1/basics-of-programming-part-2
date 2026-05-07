import json
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

from lab8 import AuthProxy, ApiKeyAuth, JWTAuth, OAuthClientCredentials

OAUTH_TOKEN = "mock-oauth-access-token"

class MockHandler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send_json(self, payload, status=200):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self._send_json({"headers": dict(self.headers)})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b""
        if self.path == "/oauth/token":
            form = dict(kv.split("=") for kv in raw.decode().split("&") if "=" in kv)
            if form.get("grant_type") == "client_credentials":
                self._send_json({"access_token": OAUTH_TOKEN, "expires_in": 3600})
            else:
                self._send_json({"error": "unsupported_grant_type"}, 400)
            return
        body = json.loads(raw) if raw else {}
        self._send_json({"headers": dict(self.headers), "json": body})

    do_PUT = do_POST
    do_DELETE = do_GET

server = HTTPServer(("127.0.0.1", 18080), MockHandler)
threading.Thread(target=server.serve_forever, daemon=True).start()
time.sleep(0.05)

BASE = "http://127.0.0.1:18080"
OAUTH_URL = BASE + "/oauth/token"

def get_auth(resp):
    h = resp.json()["headers"]
    return h.get("Authorization") or h.get("authorization")

def get_api_key(resp, name="X-API-Key"):
    h = resp.json()["headers"]
    return h.get(name) or h.get(name.lower())

print("API Key")
proxy = AuthProxy(ApiKeyAuth("my-secret-key"), base_url=BASE)
val = get_api_key(proxy.get("/headers"))
print("X-API-Key:", val)
assert val == "my-secret-key"

print("\nAPI Key (custom header)")
proxy2 = AuthProxy(ApiKeyAuth("key-B", header_name="X-Service-Token"), base_url=BASE)
val2 = get_api_key(proxy2.get("/headers"), "X-Service-Token")
print("X-Service-Token:", val2)
assert val2 == "key-B"

print("\nJWT")
proxy3 = AuthProxy(JWTAuth("my.jwt.token"), base_url=BASE)
val3 = get_auth(proxy3.get("/headers"))
print("Authorization:", val3)
assert val3 == "Bearer my.jwt.token"

print("\nOAuth 2.0 ")
proxy4 = AuthProxy(OAuthClientCredentials(OAUTH_URL, "app-id", "app-secret"), base_url=BASE)
val4 = get_auth(proxy4.get("/headers"))
print("Authorization:", val4)
assert val4 == f"Bearer {OAUTH_TOKEN}"

print("\nPOST with body")
resp = proxy3.post("/data", json={"name": "test", "value": 42})
body = resp.json()["json"]
print("Body:", body)
assert body == {"name": "test", "value": 42}

print("\nAll tests passed")