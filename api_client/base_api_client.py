import logging

import requests
from requests.exceptions import RequestException


class BaseApiClient:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def _make_request(self, method, url, headers=None, json=None):
        try:
            self.logger.info(f'Send {method} request to {url}')
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=json
            )
            response.raise_for_status()
            return response
        except RequestException:
            self.logger.error(f'Failed {method} request to {url} ')
            raise Exception(
                f'Failed {method} request to {url} '
            )

    def _get(self, url):
        return self._make_request('GET', url)

    def _post(self, url, json, headers=None):
        if headers is None:
            headers = {"Content-Type": "application/json"}
        return self._make_request('POST', url, headers=headers, json=json)

    def _patch(self, url, json, headers=None):
        if headers is None:
            headers = {"Content-Type": "application/json"}
        return self._make_request('PATCH', url, headers=headers, json=json)

    def _delete(self, url, headers=None):
        if headers is None:
            headers = {"Content-Type": "text/plain"}
        return self._make_request('DELETE', url, headers=headers)
