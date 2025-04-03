import allure
import requests
from requests.exceptions import RequestException


class BaseApiClient:
    def __init__(self, logger):
        self.logger = logger
        self.response_data = None

    def _make_request(self, method, url, headers=None, json=None):
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=json
            )
            response.raise_for_status()
            if response.status_code != 204:
                self.response_data = response.json()
            return response
        except RequestException:
            self.logger.error(f'Failed {method} request to {url} ')
            raise Exception(
                f'Failed {method} request to {url} '
            )

    def _get(self, url):
        self.logger.info(f'Send GET to {url}')
        return self._make_request('GET', url)

    def _post(self, url, json):
        self.logger.info(f'Send POST to {url}')
        headers = {"Content-Type": "application/json"}
        return self._make_request('POST', url, headers=headers, json=json)

    def _patch(self, url, json):
        self.logger.info(f'Send PATCH to {url}')
        headers = {"Content-Type": "application/json"}
        return self._make_request('PATCH', url, headers=headers, json=json)

    def _delete(self, url):
        self.logger.info(f'Send DELETE to {url}')
        headers = {"Content-Type": "text/plain"}
        return self._make_request('DELETE', url, headers=headers)
