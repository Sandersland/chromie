from __future__ import annotations
from typing import Dict
from urllib.parse import urljoin
import json
import time

import jwt
import requests


class AuthenticationError(Exception):
    pass


class GoogleWebStoreError(Exception):
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
    SCOPES = [
        "https://www.googleapis.com/auth/chromewebstore"
    ]


class GoogleWebStore:
    UPLOAD_URI = "https://www.googleapis.com/upload/chromewebstore/v1.1/items"
    METADATA_URI = "https://www.googleapis.com/chromewebstore/v1.1/items"

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

    def _handle_response(self, response: requests.Response):

    def upload(self, filepath: str) -> None:

        with open(filepath, "rb") as fh:
            response = requests.post(
                self.UPLOAD_URI,
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
                raise GoogleWebStoreError(
                    "error uploading extension:\n" + message
                )

    def publish(self, id: str) -> None:
        response = requests.post(
            "/".join([self.METADATA_URI, id, "publish"]),
            headers={
                "Authorization": "Bearer %s" % self.token.get("access_token"),
                "x-goog-api-version": "2",
                "Accept-Encoding": "gzip, deflate"
            },
        )
        if not response.ok:
            try:
                data = response.json()
                errors = data.get("error").get("message").split(";")
                raise GoogleWebStoreError(
                    "error publishing extension:\n" + "\n".join(errors)
                )
            except json.decoder.JSONDecodeError as e:
                print(response.text)
            
    def update(self, id: str, filepath: str) -> None:

        with open(filepath, "rb") as fh:
            response = requests.put(
                "/".join([self.UPLOAD_URI, id]),
                headers={
                    "Authorization": "Bearer %s" % self.token.get("access_token"),
                    "x-goog-api-version": "2",
                    "Accept-Encoding": "gzip, deflate",
                },
                data=fh.read(),
                params={"file": filepath},
            )
            data = response.json()
            if not response.ok:
                message = data.get("error").get("message")
                raise GoogleWebStoreError(
                    "error updating extension:\n" + message
                )
            if response.ok and data.get("uploadState") == "FAILURE":
                errors = data.get("itemError")
                message = "\n".join([item['error_detail'] for item in errors])
                raise GoogleWebStoreError(
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

    fp = "/Users/sandersland/dev/chromie/testy/dist/testy-0.0.2.zip"
    with open("secrets.json", "r") as file:
        SECRETS = json.load(file)

    with GoogleWebStore.session(
        "steffen@andersland.dev", credentials=SECRETS
    ) as session:
        session.update("kgbndodiiaglaldfniieoblnlpncelkp", fp)

        # session.upload(fp)
        # session.publish("kgbndodiiaglaldfniieoblnlpncelkp")
