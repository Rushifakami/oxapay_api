from typing import Optional

import requests
from .constants.api_constants import _GENERAL_API_URL, _METHODS

class SyncClient:
    def __init__(self, merchant_api_key: str, general_api_key: Optional[str] = None, timeout: Optional[int] = None):
        self._headers = {
            "merchant_api_key": merchant_api_key,
            "Content-Type": "application/json"
        }
        if general_api_key:
            self._headers["general_api_key"] = general_api_key
        self._timeout = timeout

    def request(self, method: str, endpoint: str, query_params=None, json_data=None):
        if method not in _METHODS:
            raise ValueError(f'Unsupported method "{method}".')

        url = f'{_GENERAL_API_URL}/{endpoint}'

        if method == 'GET' and query_params:
            response = requests.request(headers=self._headers, method=method, url=url, params=query_params, timeout=self._timeout)
        else:
            response = requests.request(headers=self._headers, method=method, url=url, json=json_data, timeout=self._timeout)

        if response.status_code == 200:
            if response.headers.get('content-type') == 'application/json':
                return response.json()
            else:
                return response.text
        elif response.status_code == 400:
            raise ValueError(response.json())
        else:
            raise Exception(f'Failed to make request: {response.status_code} - {response.reason}')
