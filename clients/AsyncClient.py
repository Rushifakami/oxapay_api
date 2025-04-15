import aiohttp
from .constants.api_constants import _GENERAL_API_URL, _METHODS

class AsyncClient:
    def __init__(self, merchant_api_key: str):
        self._headers = {
            "merchant_api_key": merchant_api_key,
            "Content-Type": "application/json"
        }

    async def request(self, method: str, endpoint: str, query_params=None, json_data=None):
        if method not in _METHODS:
            raise ValueError(f'Unsupported method "{method}".')

        url = f'{_GENERAL_API_URL}/{endpoint}'

        async with aiohttp.ClientSession(headers=self._headers) as session:
            if method == 'GET' and query_params:
                async with session.request(method=method, url=url, params=query_params) as response:
                    if response.status == 200:
                        if response.content_type == 'application/json':
                            return await response.json()
                        else:
                            return await response.text()
                    elif response.status == 400:
                        raise ValueError(await response.json())
                    else:
                        raise Exception(f'Failed to make request: {response.status} - {response.reason}')
            else:
                async with session.request(method=method, url=url, json=json_data) as response:
                    if response.status == 200:
                        if response.content_type == 'application/json':
                            return await response.json()
                        else:
                            return await response.text()
                    elif response.status == 400:
                        raise ValueError(await response.json())
                    else:
                        raise Exception(f'Failed to make request: {response.status} - {response.reason}.')
