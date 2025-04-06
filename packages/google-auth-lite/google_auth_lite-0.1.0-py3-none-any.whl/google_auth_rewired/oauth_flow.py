# oauth_flow.py
from requests_oauthlib import OAuth2Session
from typing import Optional
import json
import os
import webbrowser

class GoogleOAuthFlow:
    def __init__(self, client_id: str, client_secret: str, scopes: list, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = scopes
        self.redirect_uri = redirect_uri
        self.oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scopes)

    def auth_url(self) -> str:
        auth_base = "https://accounts.google.com/o/oauth2/auth"
        auth_url, _ = self.oauth.authorization_url(auth_base, access_type='offline', prompt='consent')
        return auth_url

    def fetch_token(self, response_url: str) -> dict:
        token_url = "https://oauth2.googleapis.com/token"
        token = self.oauth.fetch_token(token_url,
                                       authorization_response=response_url,
                                       client_secret=self.client_secret)
        return token

    def save_token(self, token: dict, path: str = "token.json"):
        with open(path, "w") as f:
            json.dump(token, f)

    def load_token(self, path: str = "token.json") -> Optional[dict]:
        if not os.path.exists(path):
            return None
        with open(path, "r") as f:
            return json.load(f)
