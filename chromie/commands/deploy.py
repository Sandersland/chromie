from typing import Dict
import json
import time
from urllib.parse import urlencode

import jwt
import requests


class AuthenticationError(Exception):
    pass


class BaseServiceAuth:
    TOKEN_URI = "https://oauth2.googleapis.com/token"
    SCOPES = []

    def __init__(self, credentials={}):
        self._creds = credentials

    def get_service_token(self, email: str):
        data = {
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": self._encode_token(email),
        }
        response = requests.post(
            self.TOKEN_URI,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=data
        )
        return response.json()

    def _encode_token(self, email: str):
        try:
            iat = round(time.time())
            exp = iat + 60
            payload = {
                "iss" : self.credentials.get("client_email", None),
                "sub": email,
                "scope": " ".join(self.SCOPES) if len(self.SCOPES) > 0 else "",
                "aud": self.TOKEN_URI,
                "exp": exp,
                "iat": iat,
            }
            return jwt.encode(
                payload, self.credentials.get("private_key", None), algorithm="RS256"
            )
        except TypeError as e:
            raise AuthenticationError(e)

    @property
    def credentials(self):
        return self._creds

    def set_credentials(self, **kwargs):
        for k, v in kwargs.items():
            self._creds[k] = v

    
def upload(filepath, access_token):
    url = "https://www.googleapis.com/upload/chromewebstore/v1.1/items"

    # filepath = "/Users/sandersland/dev/chromie/testy/dist/testy-0.0.1.zip"
    with open(filepath, "rb") as fh:
        response = requests.post(
            url,
            headers = {
                "Authorization": "Bearer %s" % access_token,
                "x-goog-api-version": "2",
                "Accept-Encoding": "gzip, deflate"
            },
            data=fh.read(),
            params={"file": filepath}
        )

    print(response.text)
        
def publish(id, access_token):
    url = f"https://www.googleapis.com/chromewebstore/v1.1/items/{id}/publish"


    response = requests.post(
        url,
        headers = {
            "Authorization": "Bearer %s" % access_token,
            "x-goog-api-version": "2",
            "Accept-Encoding": "gzip, deflate"
        }
    )

    print(response.text)

def update(id, filepath, access_token):
    url = f"https://www.googleapis.com/upload/chromewebstore/v1.1/items/{id}"

    # filepath = "/Users/sandersland/dev/chromie/testy/dist/testy-0.0.1.zip"
    with open(filepath, "rb") as fh:
        response = requests.put(
            url,
            headers = {
                "Authorization": "Bearer %s" % access_token,
                "x-goog-api-version": "2",
                "Accept-Encoding": "gzip, deflate"
            },
            data=fh.read(),
            params={"file": filepath}
        )

    print(response.text)


if __name__ == '__main__':

    with open("secrets.json", "r") as file:
        SECRETS = json.load(file)

    class GoogleStoreSeriveAuth(BaseServiceAuth):
        SCOPES = [
            "https://www.googleapis.com/auth/chromewebstore"
        ]

    auth = GoogleStoreSeriveAuth()

    auth.set_credentials(**SECRETS)

    try:
        token_dict = auth.get_service_token("steffen@andersland.dev")
        access_token = token_dict.get("access_token")
        print(access_token)
    except AuthenticationError as e:
        print(e)
    fp = "/Users/sandersland/dev/chromie/testy/dist/testy-0.0.1.zip"

    publish("ejianacolgbhmddlbgeldegfdmcdemdf", access_token)