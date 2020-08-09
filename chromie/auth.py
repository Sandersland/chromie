from typing import List, Dict
import time

import requests
import jwt


class AuthenticationError(Exception):
    pass


class BaseServiceAuth:
    TOKEN_URI = "https://oauth2.googleapis.com/token"
    SCOPES = []

    def __init__(self, credentials: Dict[str, str] = None):
        self._creds = credentials if credentials else {}

    @classmethod
    def add_scopes(cls, scopes: List[str]) -> None:
        cls.SCOPES.extend(scopes)

    def get_token(self, email: str) -> str:
        data = {
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": self._encode_web_token(email),
        }
        response = requests.post(
            self.TOKEN_URI,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=data,
        )
        return response.json().get("access_token")

    def _encode_web_token(self, email: str) -> str:
        try:
            iat = round(time.time())
            exp = iat + 60
            payload = {
                "iss": self._creds.get("client_email", None),
                "sub": email,
                "scope": " ".join(self.SCOPES) if len(self.SCOPES) > 0 else "",
                "aud": self.TOKEN_URI,
                "exp": exp,
                "iat": iat,
            }
            return jwt.encode(
                payload, self._creds.get("private_key", None), algorithm="RS256"
            )
        except TypeError as e:
            raise AuthenticationError(e)

    def set_credentials(self, **kwargs: str) -> None:
        for k, v in kwargs.items():
            self._creds[k] = v
