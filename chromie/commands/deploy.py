import json
import time

import jwt
import requests


class AuthenticationError(Exception):
    pass


class BaseServiceAuth:
    TOKEN_URI = "https://oauth2.googleapis.com/token"
    SCOPES = []

    def __init__(self, credentials={}):
        self._creds = credentials
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

    def __init__(self):
        # self.access_token = None
        self.token = None

    def authenticate(self, email, credentials):
        with open("secrets.json", "r") as file:
            SECRETS = json.load(file)

        auth = GoogleWebStoreAuthentication()
        auth.set_credentials(**credentials)

        self.token = auth.set_token(email)

    def upload(self, filepath):
        url = "https://www.googleapis.com/upload/chromewebstore/v1.1/items"

        with open(filepath, "rb") as fh:
            response = requests.post(
                url,
                headers={
                    "Authorization": "Bearer %s" % self.token.get("access_token"),
                    "x-goog-api-version": "2",
                    "Accept-Encoding": "gzip, deflate",
                },
                data=fh.read(),
                params={"file": filepath},
            )

        print(response.text)

    def publish(self, id):
        url = f"https://www.googleapis.com/chromewebstore/v1.1/items/{id}/publish"

        response = requests.post(
            url,
            headers={
                "Authorization": "Bearer %s" % self.token.get("access_token"),
                "x-goog-api-version": "2",
                "Accept-Encoding": "gzip, deflate",
            },
        )

        print(response.text)

    def update(self, id, filepath):
        url = f"https://www.googleapis.com/upload/chromewebstore/v1.1/items/{id}"
        with open(filepath, "rb") as fh:
            response = requests.put(
                url,
                headers={
                    "Authorization": "Bearer %s" % self.token.get("access_token"),
                    "x-goog-api-version": "2",
                    "Accept-Encoding": "gzip, deflate",
                },
                data=fh.read(),
                params={"file": filepath},
            )

        print(response.text)


if __name__ == "__main__":

    fp = "/Users/sandersland/dev/chromie/testy/dist/testy-0.0.1.zip"
    with open("secrets.json", "r") as file:
        SECRETS = json.load(file)

    session = GoogleWebStore()
    session.authenticate("steffen@andersland.dev", credentials=SECRETS)
    session.upload(fp)
