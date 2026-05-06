import requests
from abc import ABC, abstractmethod

class AuthStrategy(ABC):
    @abstractmethod
    def get_headers(self) -> dict:
        pass

class ApiKeyAuth(AuthStrategy):
    def __init__(self, api_key: str, header_name: str = "X-API-Key"):
        self._api_key = api_key
        self._header_name = header_name

    def get_headers(self) -> dict:
        return {self._header_name: self._api_key}

class JWTAuth(AuthStrategy):
    def __init__(self, token: str):
        self._token = token

    def get_headers(self) -> dict:
        return {"Authorization": f"Bearer {self._token}"}

class OAuthClientCredentials(AuthStrategy):
    def __init__(self, token_url: str, client_id: str, client_secret: str, scope: str = ""):
        self._token_url = token_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._scope = scope
        self._access_token = None

    def _fetch_token(self):
        resp = requests.post(
            self._token_url,
            data={
                "grant_type": "client_credentials",
                "client_id": self._client_id,
                "client_secret": self._client_secret,
                "scope": self._scope,
            },
            timeout=10,
        )
        resp.raise_for_status()
        self._access_token = resp.json()["access_token"]

    def get_headers(self) -> dict:
        if not self._access_token:
            self._fetch_token()
        return {"Authorization": f"Bearer {self._access_token}"}

class AuthProxy:
    def __init__(self, strategy: AuthStrategy, base_url: str = "", timeout: int = 15):
        self._strategy = strategy
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._session = requests.Session()

    def request(self, method: str, url: str, extra_headers: dict = None, **kwargs) -> requests.Response:
        full_url = (self._base_url + url) if self._base_url else url
        headers = dict(extra_headers or {})
        headers.update(self._strategy.get_headers())
        return self._session.request(method.upper(), full_url, headers=headers, timeout=self._timeout, **kwargs)

    def get(self, url: str, **kwargs) -> requests.Response:
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs) -> requests.Response:
        return self.request("POST", url, **kwargs)

    def put(self, url: str, **kwargs) -> requests.Response:
        return self.request("PUT", url, **kwargs)

    def delete(self, url: str, **kwargs) -> requests.Response:
        return self.request("DELETE", url, **kwargs)

    def patch(self, url: str, **kwargs) -> requests.Response:
        return self.request("PATCH", url, **kwargs)