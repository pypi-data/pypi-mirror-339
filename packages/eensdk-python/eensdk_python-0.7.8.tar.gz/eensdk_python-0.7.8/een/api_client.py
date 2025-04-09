import json
import importlib
import importlib.resources as pkg_resources
import inspect
import time
import requests
import logging
import urllib.parse
from abc import ABC, abstractmethod
from requests.exceptions import RequestException
from een.exceptions import AuthenticationError


class TokenStorage(ABC):
    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def set(self, key, value):
        pass

    @abstractmethod
    def __contains__(self, key):
        pass


class EENClient:
    auth_url = "https://auth.eagleeyenetworks.com/oauth2/authorize"

    def __init__(
            self, client_id, client_secret, redirect_uri,
            token_storage, max_retries=3, timeout=10):
        if not isinstance(token_storage, TokenStorage):
            raise TypeError(
                "token_storage must implement the TokenStorage interface.")
        self.client_id = client_id
        self.client_secret = client_secret
        self.max_retries = max_retries
        self.timeout = timeout
        self.redirect_uri = redirect_uri
        self.token_storage = token_storage

        self.logger = logging.getLogger(__name__)

        self._load_resources()

    def _load_resources(self):
        resources_dir = pkg_resources.files('een.resources')
        for resource in resources_dir.iterdir():
            if resource.is_file() and resource.name.endswith('.py') and resource.name != '__init__.py':
                module_name = f"een.resources.{resource.name[:-3]}"
                module = importlib.import_module(module_name)
                for name, func in inspect.getmembers(
                    module, inspect.isfunction
                ):
                    setattr(self, name, func.__get__(self))

    def __retry_request(self, request_func, *args, **kwargs):
        max_retries = self.max_retries
        retry_count = 0
        while retry_count <= max_retries:
            try:
                response = request_func(*args, **kwargs)
                if response.ok:
                    return response
                elif response.status_code == 401:
                    self.logger.info("Auth failed. Refreshing Access Token.")
                    self.refresh_access_token()
                else:
                    raise Exception(
                        f"{response.status_code} Response: {response.text}")
            except (AuthenticationError, RequestException) as e:
                self.logger.error(
                    f"Request failed: {e}. {retry_count}/{max_retries}")
                if retry_count == max_retries:
                    raise
                retry_count += 1
                time.sleep(2 ** retry_count)

    # API Call
    # This function will make an API call to the Eagle Eye Networks API
    def _api_call(
            self,
            endpoint,
            method='GET',
            params=None,
            data=None,
            headers=None,
            stream=False
            ):
        base_url = self.token_storage.get('base_url')

        url = f"https://{base_url}/api/v3.0{endpoint}"
        if params:
            url += '?' + urllib.parse.urlencode(params)

        self.logger.info(f"request: {url}")

        if not headers:
            headers = {
                "accept": "application/json",
                "content-type": "application/json"
            }

        def request_func():
            token = self.token_storage.get('access_token')
            local_headers = headers.copy()
            local_headers['Authorization'] = f"Bearer {token}"
            if method == 'GET':
                return requests.get(
                    url, headers=local_headers,
                    stream=stream, timeout=self.timeout
                )
            if method == 'DELETE':
                return requests.delete(
                    url, headers=local_headers, timeout=self.timeout
                )
            elif method == 'POST':
                return requests.post(
                    url, headers=local_headers,
                    data=json.dumps(data), timeout=self.timeout
                )
            elif method == 'PUT':
                return requests.put(
                    url, headers=local_headers,
                    data=json.dumps(data), timeout=self.timeout
                )
            elif method == 'PATCH':
                return requests.patch(
                    url, headers=local_headers,
                    data=json.dumps(data), timeout=self.timeout
                )

        response = self.__retry_request(request_func)
        if stream:
            return response
        return response.text

    def get_auth_url(self):
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "scope": "vms.all",
            "redirect_uri": self.redirect_uri
        }
        return self.auth_url + '?' + urllib.parse.urlencode(params)

    # OAuth Authentication
    def auth_een(self, token, type="code"):
        """
        Authenticate with the Eagle Eye Networks API
        and store the access token, refresh token,
        and base URL in the token storage.

        :param token: The authorization code or refresh token.
        :param type: The type of token being used. Either 'code' or 'refresh'.
        :return: The response from the authentication request.
        """
        url = "https://auth.eagleeyenetworks.com/oauth2/token"
        headers = {
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded"
        }

        if type == "code":
            data = {
                "grant_type": "authorization_code",
                "scope": "vms.all",
                "code": token,
                "redirect_uri": self.redirect_uri
            }
        elif type == "refresh":
            data = {
                "grant_type": "refresh_token",
                "scope": "vms.all",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": token
            }
        else:
            raise Exception("Invalid auth type")
        response = requests.post(
            url,
            auth=(
                self.client_id,
                self.client_secret
            ),
            data=data,
            headers=headers,
            timeout=self.timeout
        )
        if response.ok:
            auth_response = json.loads(response.text)
            self.token_storage.set(
                'access_token', auth_response['access_token'])
            self.token_storage.set(
                'refresh_token', auth_response['refresh_token'])
            self.token_storage.set(
                'base_url', auth_response['httpsBaseUrl']['hostname'])
        else:
            raise AuthenticationError(
                "Authentication Failed: {code} {text}".format(
                    code=response.status_code,
                    text=response.text
                ))
        return response

    def refresh_access_token(self):
        refresh_token = self.token_storage.get('refresh_token')
        if not refresh_token:
            raise AuthenticationError("No refresh token found.")
        self.auth_een(refresh_token, type="refresh")

    def revoke_refresh_token(self, refresh_token: str=None):
        if refresh_token is None:
            refresh_token = self.token_storage.get('refresh_token')
        if not refresh_token:
            raise AuthenticationError("No refresh token found.")
        url = "https://auth.eagleeyenetworks.com/oauth2/revoke"
        headers = {
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded"
        }
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "token": refresh_token
        }
        response = requests.post(
            url, data=data, headers=headers, timeout=self.timeout)
        return response
