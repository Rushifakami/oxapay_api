import aiohttp
from .constants.api_constants import _GENERAL_API_URL, _METHODS

class AsyncClient():
    async def request(self, method: str, endpoint: str, json_data=None):
        if method not in _METHODS:
            raise ValueError(f'Unsupported method "{method}".')
        async with aiohttp.ClientSession() as session:
            url = f'{_GENERAL_API_URL}/{endpoint}'
            async with session.request(method, url, json=json_data) as response:
                if response.status == 200:
                    if response.content_type == 'application/json':
                        return await response.json()
                    else:
                        return await response.text()
                else:
                    raise Exception(f'Failed to make request: {response.status} - {response.reason}')