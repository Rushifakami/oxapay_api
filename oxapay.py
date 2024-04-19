import aiohttp
from utils.response_models import PaymentStatus, OrderStatus

GENERAL_API_URL = 'https://api.oxapay.com/'

class OxaPay:
    def __init__(self, merchant_api_key: str, sandbox: bool = False):
        self.merchant_api_key = merchant_api_key
        self.sandbox = sandbox

    async def check_api_status(self):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(f'{GENERAL_API_URL}/monitor') as response:
                    result = await response.text()
                    return result
            except Exception as e:
                raise Exception

    async def create_invoice(
            self,
            amount: float,
            currency: str = None,
            callbackUrl: str = None,
            underPaidCover: float = None,
            feePaidByPayer: float = 0,  # default 0
            lifeTime: int = 60,  # default 60
            email: str = None,
            orderId: str = None,
            description: str = None,
            returnUrl: str = None,
            raw_response: bool = False  # Flag to request a raw response
    ):
        if feePaidByPayer not in {0, 1}:
            raise ValueError("feePaidByPayer should be either 0 or 1")
        if not 15 <= lifeTime <= 2880:
            raise ValueError("lifeTime should be between 15 and 2880")

        merchant = 'sandbox' if self.sandbox else self.merchant_api_key
        async with aiohttp.ClientSession() as session:
            invoice_data = {
                'merchant': merchant,
                'amount': amount,
                'currency': currency,
                'callbackUrl': callbackUrl,
                'underPaidCover': underPaidCover,
                'feePaidByPayer': feePaidByPayer,
                'lifeTime': lifeTime,
                'email': email,
                'orderId': orderId,
                'description': description,
                'returnUrl': returnUrl
            }
            try:
                async with session.post(f'{GENERAL_API_URL}/merchants/request', json=invoice_data) as response:
                    data = await response.json()
                    if raw_response:
                        return data
                    else:
                        return OrderStatus(**data)
            except Exception:
                raise Exception

    async def get_supported_currencies(self):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(f'{GENERAL_API_URL}/api/currencies') as response:
                    data = await response.json()
                    return data
            except Exception:
                raise Exception

    async def get_supported_networks(self):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(f'{GENERAL_API_URL}/api/networks') as response:
                    result = await response.json()
                    return result
            except Exception:
                raise Exception

    async def get_supported_fiat_currencies(self):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(f'{GENERAL_API_URL}/api/fiats') as response:
                    result = await response.json()
                    return result
            except Exception:
                raise Exception

    async def get_payment_information(self, trackId: int, raw_response: bool = False):
        merchant = 'sandbox' if self.sandbox else self.merchant_api_key
        async with aiohttp.ClientSession() as session:
            payment_data = {
                'merchant': merchant,
                'trackId': trackId
            }
            try:
                async with session.post(f'{GENERAL_API_URL}/merchants/inquiry', json=payment_data) as response:
                    data = await response.json()
                    if raw_response:
                        return data
                    else:
                        return PaymentStatus(**data)
            except Exception:
                raise Exception

    async def create_white_label_payment(
            self,
            amount: float,
            payCurrency: str,
            callbackUrl: str = None,
            payAmount: float = None,
            currency: str = None,
            email: str = None,
            orderId: str = None,
            description: str = None,
            underPaidCover: float = None,
            feePaidByPayer: float = None,
            lifeTime: int = None,
            network: str = None
    ):
        async with aiohttp.ClientSession() as session:
            payment_data = {
                'merchant': self.merchant_api_key,
                'amount': amount,
                'payCurrency': payCurrency,
                'callbackUrl': callbackUrl,
                'payAmount': payAmount,
                'currency': currency,
                'email': email,
                'orderId': orderId,
                'description': description,
                'underPaidCover': underPaidCover,
                'feePaidByPayer': feePaidByPayer,
                'lifeTime': lifeTime,
                'network': network
            }
            try:
                async with session.post(f'{GENERAL_API_URL}/merchants/request/whitelabel', json=payment_data) as response:
                    data = await response.json()
                    return data
            except Exception:
                raise Exception

    async def create_static_address(
            self,
            currency: str,
            callbackUrl: str = None,
            network: str = None
    ):
        async with aiohttp.ClientSession() as session:
            static_address_data = {
                'merchant': self.merchant_api_key,
                'currency': currency,
                'callbackUrl': callbackUrl,
                'network': network
            }
            try:
                async with session.post(f'{GENERAL_API_URL}/merchants/request/staticaddress', json=static_address_data) as response:
                    data = await response.json()
                    return data
            except Exception:
                raise Exception

    async def revoke_static_wallet(self, address: str):
        async with aiohttp.ClientSession() as session:
            data = {
                'merchant': self.merchant_api_key,
                'address': address
            }
            try:
                async with session.post(f'{GENERAL_API_URL}/merchants/revoke/staticaddress', json=data) as response:
                    result = await response.json()
                    return result
            except Exception:
                raise Exception

    async def get_payment_history(
            self,
            orderBy: str = 'desc',
            sortBy: str = 'create_date',
            trackId: int = None,
            page: int = 1,
            size: int = 10,
            orderId: str = None,
            status: str = None,
            feePaidByPayer: float = None,
            type: str = None,
            network: str = None,
            payCurrency: str = None,
            currency: str = None,
            toAmount: float = None,
            fromAmount: float = None,
            toDate: str = None,
            fromDate: str = None,
            address: str = None,
            txID: str = None
    ):
        async with aiohttp.ClientSession() as session:
            data = {
                'merchant': self.merchant_api_key,
                'orderBy': orderBy,
                'sortBy': sortBy,
                'trackId': trackId,
                'page': page,
                'size': size,
                'orderId': orderId,
                'status': status,
                'feePaidByPayer': feePaidByPayer,
                'type': type,
                'network': network,
                'payCurrency': payCurrency,
                'currency': currency,
                'toAmount': toAmount,
                'fromAmount': fromAmount,
                'toDate': toDate,
                'fromDate': fromDate,
                'address': address,
                'txID': txID
            }
            try:
                async with session.post(f'{GENERAL_API_URL}/merchants/list', json=data) as response:
                    result = await response.json()
                    return result
            except Exception:
                raise Exception

    async def get_accepted_coins(self):
        async with aiohttp.ClientSession() as session:
            data = {'merchant': self.merchant_api_key}
            try:
                async with session.post(f'{GENERAL_API_URL}/merchants/allowedCoins', json=data) as response:
                    result = await response.json()
                    return result
            except Exception:
                raise Exception

    async def get_prices(self):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(f'{GENERAL_API_URL}/api/prices') as response:
                    result = await response.json()
                    return result
            except Exception:
                raise Exception

    async def get_exchange_rate(self, from_currency: str, to_currency: str):
        async with aiohttp.ClientSession() as session:
            exchange_data = {
                'fromCurrency': from_currency,
                'toCurrency': to_currency
            }
            try:
                async with session.post(f'{GENERAL_API_URL}/exchange/rate', json=exchange_data) as response:
                    result = await response.json()
                    return result
            except Exception:
                raise Exception

    async def calculate_exchange(self, from_currency: str, to_currency: str, amount: float):
        async with aiohttp.ClientSession() as session:
            exchange_data = {
                'fromCurrency': from_currency,
                'toCurrency': to_currency,
                'amount': amount
            }
            try:
                async with session.post(f'{GENERAL_API_URL}/exchange/calculate', json=exchange_data) as response:
                    result = await response.json()
                    return result
            except Exception:
                raise Exception

    async def get_exchange_pairs(self):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(f'{GENERAL_API_URL}/api/pairs') as response:
                    result = await response.json()
                    return result
            except Exception:
                raise Exception
