from __future__ import annotations
import json
import time
from typing import Dict
import jwt
import requests


class AuthenticationError(Exception):
    pass


class GoogleWebStoreError(Exception):
    pass


class GoogleWebStorePublishingError(GoogleWebStoreError):
    pass


class GoogleWebStoreUploadingError(GoogleWebStoreError):
    pass


class GoogleWebStoreUpadateError(GoogleWebStoreError):
    pass


class BaseServiceAuth:
    TOKEN_URI = "https://oauth2.googleapis.com/token"
    SCOPES = []

    def __init__(self, credentials=None):
        self._creds = credentials if credentials else {}
        self.token = None

    def set_token(self, email: str):
        data = {
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": self._encode_web_token(email),
        }
        response = requests.post(
            self.TOKEN_URI,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=data,
        )
        self.token = response.json()
        return self.token

    def _encode_web_token(self, email: str):
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

    def set_credentials(self, **kwargs):
        for k, v in kwargs.items():
            self._creds[k] = v


class GoogleWebStoreAuthentication(BaseServiceAuth):
    SCOPES = ["https://www.googleapis.com/auth/chromewebstore"]


class GoogleWebStore:
    URLS = {
        "publish": "https://www.googleapis.com/chromewebstore/v1.1/items/{}/publish/",
        "upload": "https://www.googleapis.com/upload/chromewebstore/v1.1/items/",
    }

    def __init__(self) -> GoogleWebStore:
        self.token = None

    @staticmethod
    def session(email, credentials):
        return GoogleWebStoreSession(email, credentials)

    def authenticate(self, email, credentials) -> None:
        auth = GoogleWebStoreAuthentication()
        auth.set_credentials(**credentials)
        self.token = auth.set_token(email)
        return None

    def upload(self, filepath: str) -> None:

        with open(filepath, "rb") as fh:
            response = requests.post(
                self.URLS.get("upload"),
                headers={
                    "Authorization": "Bearer %s" % self.token.get("access_token"),
                    "x-goog-api-version": "2",
                    "Accept-Encoding": "gzip, deflate",
                },
                data=fh.read(),
                params={"file": filepath},
            )
            if not response.ok:
                message = response.json().get("error").get("message")
                raise GoogleWebStoreUploadingError(
                    "error uploading extension:\n" + message
                )

    def publish(self, id: str) -> None:
        response = requests.post(
            self.URLS.get("publish").format(id),
            headers={
                "Authorization": "Bearer %s" % self.token.get("access_token"),
                "x-goog-api-version": "2",
                "Accept-Encoding": "gzip, deflate",
            },
        )
        if not response.ok:
            errors = response.json().get("error").get("message").split(";")
            raise GoogleWebStorePublishingError(
                "error publishing extension:\n" + "\n".join(errors)
            )

    def update(self, id: str, filepath: str) -> None:

        with open(filepath, "rb") as fh:
            response = requests.put(
                self.URLS.get("upload") + id,
                headers={
                    "Authorization": "Bearer %s" % self.token.get("access_token"),
                    "x-goog-api-version": "2",
                    "Accept-Encoding": "gzip, deflate",
                },
                data=fh.read(),
                params={"file": filepath},
            )
            if not response.ok:
                message = response.json().get("error").get("message")
                raise GoogleWebStoreUpadateError(
                    "error updating extension:\n" + message
                )


class GoogleWebStoreSession:
    def __init__(self, email: str, credentials: Dict[str, str]) -> GoogleWebStoreSession:
        self.email = email
        self.credentials = credentials
        self.store = None

    def __enter__(self) -> GoogleWebStore:
        self.store = GoogleWebStore()
        self.store.authenticate(self.email, self.credentials)
        return self.store

    def __exit__(self, *args):
        return None


if __name__ == "__main__":

    fp = "/Users/sandersland/dev/chromie/testy/dist/testy-0.0.1.zip"
    with open("secrets.json", "r") as file:
        SECRETS = json.load(file)

    with GoogleWebStore.session(
        "steffen@andersland.dev", credentials=SECRETS
    ) as session:
        # is_successful = session.update("pdopgpiphmmkcofbgcbeiaeochdogcok", fp)
        # is_successful = session.upload(fp)
        is_successful = session.publish("pdopgpiphmmkcofbgcbeiaeochdogcok")

        print(is_successful)
