from __future__ import annotations
from typing import Dict
from json.decoder import JSONDecodeError

import requests

from chromie.auth import BaseServiceAuth


class GoogleWebStoreError(Exception):
    pass


class GoogleWebStoreAuthentication(BaseServiceAuth):
    SCOPES = ["https://www.googleapis.com/auth/chromewebstore"]


class GoogleWebStore:
    UPLOAD_URI = "https://www.googleapis.com/upload/chromewebstore/v1.1/items"
    METADATA_URI = "https://www.googleapis.com/chromewebstore/v1.1/items"

    def __init__(
        self, token: Dict[str, str] = None, session: requests.Session = None
    ) -> GoogleWebStore:
        self.token = token
        self._request_session = session if session else requests.Session()

    @staticmethod
    def session(email: str, credentials: Dict[str, str]) -> GoogleWebStoreSession:
        return GoogleWebStoreSession(email, credentials)

    def authenticate(self, email: str, credentials: Dict[str, str]) -> None:
        auth = GoogleWebStoreAuthentication()
        auth.set_credentials(**credentials)
        self.token = auth.get_token(email)
        return None

    def _make_request(self, request: requests.PreparedRequest) -> requests.Response:
        return self._request_session.send(request)

    def _build_request(
        self, method: str, url: str, fp: str = None
    ) -> requests.PreparedRequest:
        request = requests.Request(method=method, url=url)
        headers = {
            "Authorization": "Bearer {}".format(self.token),
            "x-goog-api-version": "2",
        }
        if fp:
            with open(fp, "rb") as file:
                request.data = file.read()
                request.params = {"file": fp}
                headers["Accept-Encoding"] = "gzip, deflate"
        request.headers = headers
        return request.prepare()

    def _handle_response(self, response: requests.Response) -> str:
        try:
            data = response.json()
            if not response.ok:
                errors = data.get("error").get("message").split(";")
                if len(errors) == 1:
                    raise GoogleWebStoreError(errors[0])
                message = "\n  " + "\n  ".join(
                    [
                        f"{i}. {err.split(':')[1].strip()}"
                        if ":" in err and "http" not in err
                        else f"{i}. {err.strip()}"
                        for i, err in enumerate(errors, 1)
                    ]
                )
                raise GoogleWebStoreError(message)
            elif response.ok and data.get("uploadState") == "FAILURE":
                errors = data.get("itemError")
                message = f"\n" + "\n".join(
                    [
                        f"{i}. {err.get('error_detail')}"
                        for i, err in enumerate(errors, 1)
                    ]
                )
                raise GoogleWebStoreError(message)
            elif response.ok and data.get("uploadState") == "SUCCESS":
                return data.get("id")
        except JSONDecodeError:
            raise GoogleWebStoreError(response.text)

    def upload(self, filepath: str) -> str:
        request = self._build_request("POST", url=self.UPLOAD_URI, fp=filepath)
        response = self._make_request(request)
        return self._handle_response(response)

    def publish(self, id: str) -> str:
        url = "/".join([self.METADATA_URI, id, "publish"])
        request = self._build_request(method="POST", url=url)
        response = self._make_request(request)
        return self._handle_response(response)

    def update(self, id: str, filepath: str) -> str:
        url = "/".join([self.UPLOAD_URI, id])
        request = self._build_request(method="PUT", url=url, fp=filepath)
        response = self._make_request(request)
        return self._handle_response(response)


class GoogleWebStoreSession:
    def __init__(
        self, email: str, credentials: Dict[str, str], session: requests.Session = None
    ) -> GoogleWebStoreSession:
        self.email = email
        self.credentials = credentials
        self.session = session
        self.store = None

    def __enter__(self) -> GoogleWebStore:
        self.store = GoogleWebStore(session=self.session)
        self.store.authenticate(self.email, self.credentials)
        return self.store

    def __exit__(self, *args):
        return None
