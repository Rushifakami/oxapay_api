from .clients.SyncClient import SyncClient
from .utils.response_models import PaymentStatus, OrderStatus

class SyncOxaPay:
    def __init__(self, merchant_api_key: str, sandbox: bool = False):
        self.merchant_api_key = merchant_api_key
        self.sandbox = sandbox
        self.client = SyncClient()

    def check_api_status(self):
        try:
            return self.client.request('POST', 'monitor')
        except Exception:
            raise Exception

    def create_invoice(
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
            response_data = self.client.request('POST', 'merchants/request', json_data=invoice_data)
            if raw_response:
                return response_data
            else:
                return OrderStatus(**response_data)
        except Exception:
            raise Exception

    def get_supported_currencies(self):
        try:
            return self.client.request('POST', 'api/currencies')
        except Exception:
            raise Exception

    def get_supported_networks(self):
        try:
            return self.client.request('POST', 'api/networks')
        except Exception:
            raise Exception

    def get_supported_fiat_currencies(self):
        try:
            return self.client.request('POST', 'api/fiats')
        except Exception:
            raise Exception

    def get_payment_information(self, trackId: int, raw_response: bool = False):
        merchant = 'sandbox' if self.sandbox else self.merchant_api_key
        payment_data = {
            'merchant': merchant,
            'trackId': trackId
        }
        try:
            response_data = self.client.request('POST', 'merchants/inquiry', json_data=payment_data)
            if raw_response:
                return response_data
            else:
                return PaymentStatus(**response_data)
        except Exception:
            raise Exception

    def create_white_label_payment(
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
            return self.client.request('POST', 'merchants/request/whitelabel', json_data=payment_data)
        except Exception:
            raise Exception

    def create_static_address(
            self,
            currency: str,
            callbackUrl: str = None,
            network: str = None
    ):
        static_address_data = {
            'merchant': self.merchant_api_key,
            'currency': currency,
            'callbackUrl': callbackUrl,
            'network': network
        }
        try:
            return self.client.request('POST', 'merchants/request/staticaddress', json_data=static_address_data)
        except Exception:
            raise Exception

    def revoke_static_wallet(self, address: str):
        data = {
            'merchant': self.merchant_api_key,
            'address': address
        }
        try:
            return self.client.request('POST', 'merchants/revoke/staticaddress', json_data=data)
        except Exception:
            raise Exception

    def get_payment_history(
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
            return self.client.request('POST', 'merchants/list', json_data=data)
        except Exception:
            raise Exception

    def get_accepted_coins(self):
        data = {'merchant': self.merchant_api_key}
        try:
            return self.client.request('POST', 'merchants/allowedCoins', json_data=data)
        except Exception:
            raise Exception

    def get_prices(self):
        try:
            return self.client.request('POST', 'api/prices')
        except Exception:
            raise Exception

    def get_exchange_rate(self, from_currency: str, to_currency: str):
        try:
            exchange_data = {
                'fromCurrency': from_currency,
                'toCurrency': to_currency
            }
            return self.client.request('POST', 'exchange/rate', json_data=exchange_data)
        except Exception:
            raise Exception

    def calculate_exchange(self, from_currency: str, to_currency: str, amount: float):
        try:
            exchange_data = {
                'fromCurrency': from_currency,
                'toCurrency': to_currency,
                'amount': amount
            }
            return self.client.request('POST', 'exchange/calculate', json_data=exchange_data)
        except Exception:
            raise Exception

    def get_exchange_pairs(self):
        try:
            return self.client.request('POST', 'api/pairs')
        except Exception:
            raise Exception
