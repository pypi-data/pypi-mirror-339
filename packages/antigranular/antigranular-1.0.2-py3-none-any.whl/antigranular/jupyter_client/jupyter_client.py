import requests

from antigranular.config import config


class JupyterClient:
    """Class to maintain connection/session with Jupyter Server. All the calls to JS will go via this class."""

    def __init__(
        self,
        client_id,
        client_secret,
        headers={},
    ):
        self.url = config.AG_ENCLAVE_URL
        self.base_url = self.url
        self.token_url = config.AG_OAUTH_URL
        self.session = requests.Session()
        if headers:
            self.session.headers.update(headers)
        self._get_token(client_id, client_secret)

    def get(self, endpoint, data=None, json=None, params=None, headers=None):
        return self._make_request(
            "GET", endpoint, data=data, json=json, params=params, headers=headers
        )

    def post(
        self, endpoint, data=None, json=None, params=None, headers=None, files=None
    ):
        return self._make_request(
            "POST",
            endpoint,
            data=data,
            json=json,
            params=params,
            headers=headers,
            files=files,
        )

    def put(self, endpoint, data=None, json=None, params=None, headers=None):
        return self._make_request(
            "PUT", endpoint, data=data, json=json, params=params, headers=headers
        )

    def delete(self, endpoint, data=None, json=None, params=None, headers=None):
        return self._make_request(
            "DELETE", endpoint, data=data, json=json, params=params, headers=headers
        )

    def _make_request(
        self,
        method,
        endpoint,
        data=None,
        json=None,
        params=None,
        headers=None,
        files=None,
    ):
        verify = True
        if headers:
            with self.session as s:
                s.headers.update(headers)
                response = s.request(
                    method,
                    endpoint,
                    data=data,
                    json=json,
                    params=params,
                    files=files,
                    verify=verify,
                )
                s.headers.update(self.session.headers)
        else:
            response = self.session.request(
                method, endpoint, data=data, json=json, params=params, verify=verify
            )
        return response

    def _get_token(self, client_id: str, client_secret: str):
        res = requests.post(
            self.token_url,
            json={"client_id": client_id, "client_secret": client_secret},
        )
        res.raise_for_status()
        data = res.json()
        self.session.headers["Authorization"] = data.get("access_token")
        return data.get("access_token")


def get_jupyter_client(client_id: str, client_secret: str):
    return JupyterClient(client_id, client_secret)
