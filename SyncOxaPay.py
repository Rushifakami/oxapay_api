from .clients.SyncClient import SyncClient
from .utils.response_models import PaymentStatus, OrderStatus

class SyncOxaPay:
    def __init__(self, merchant_api_key: str):
        """
        :param merchant_api_key: The merchant's API key for authentication
        """
        self.merchant_api_key = merchant_api_key
        self._client = SyncClient(self.merchant_api_key)

    def get_api_status(self):
        """
        Get the current status of the OxaPay API
        :return: The API status information
        """
        try:
            return self._client.request('GET', 'common/monitor')
        except Exception:
            raise Exception

    def create_invoice(
            self,
            amount: float,
            currency: str = None,
            lifetime: int = 60,
            fee_paid_by_payer: float = None,
            under_paid_coverage: float = None,
            to_currency: str = "USDT",
            auto_withdrawal: bool = False,
            mixed_payment: bool = None,
            callback_url: str = None,
            return_url: str = None,
            email: str = None,
            order_id: str = None,
            thanks_message: str = None,
            description: str = None,
            sandbox: bool = False,
            raw_response: bool = False
    ):
        """

        :param amount:
        :param currency:
        :param lifetime:
        :param fee_paid_by_payer:
        :param under_paid_coverage:
        :param to_currency:
        :param auto_withdrawal:
        :param mixed_payment:
        :param callback_url:
        :param return_url:
        :param email:
        :param order_id:
        :param thanks_message:
        :param description:
        :param sandbox:
        :param raw_response:
        :return:
        """
        invoice_data = {
            'amount': amount,
            'lifetime': lifetime,
            'auto_withdrawal': auto_withdrawal,
        }

        if currency is not None:
            invoice_data['currency'] = currency
        if fee_paid_by_payer is not None:
            invoice_data['fee_paid_by_payer'] = fee_paid_by_payer
        if under_paid_coverage is not None:
            invoice_data['under_paid_coverage'] = under_paid_coverage
        if to_currency is not None:
            invoice_data['to_currency'] = to_currency
        if mixed_payment is not None:
            invoice_data['mixed_payment'] = mixed_payment
        if callback_url is not None:
            invoice_data['callback_url'] = callback_url
        if return_url is not None:
            invoice_data['return_url'] = return_url
        if email is not None:
            invoice_data['email'] = email
        if order_id is not None:
            invoice_data['order_id'] = order_id
        if thanks_message is not None:
            invoice_data['thanks_message'] = thanks_message
        if description is not None:
            invoice_data['description'] = description
        if sandbox is not None:
            invoice_data['sandbox'] = sandbox

        try:
            response_data = self._client.request('POST', 'payment/invoice', json_data=invoice_data)
            if raw_response:
                return response_data
            else:
                return OrderStatus(**response_data["data"])
        except Exception as e:
            raise Exception(f"Error creating invoice: {e}")

    def get_supported_currencies(self):
        """
        Retrieves a list of supported currencies and their network details.

        :return: A list of supported currencies with their details.
        """
        try:
            return self._client.request('GET', 'common/currencies')
        except Exception:
            raise Exception

    def get_supported_networks(self):
        """
        Retrieves a list of supported blockchain networks for cryptocurrency transactions.

        :return: A list of supported blockchain networks.
        """
        try:
            return self._client.request('GET', 'common/networks')
        except Exception:
            raise Exception

    def get_supported_fiat_currencies(self):
        """
        Retrieves a list of supported fiat currencies and their details.

        :return: A list of supported fiat currencies with their details.
        """
        try:
            return self._client.request('GET', 'common/fiats')
        except Exception:
            raise Exception

    def get_payment_information(self, track_id: int, raw_response: bool = False):
        """

        :param track_id:
        :param raw_response:
        :return:
        """
        try:
            response_data = self._client.request('GET', f'payment/{track_id}')
            if raw_response:
                return response_data
            else:
                return PaymentStatus(**response_data["data"])
        except Exception:
            raise Exception

    def create_white_label_payment(
            self,
            amount: float,
            pay_currency: str,
            callback_url: str = None,
            currency: str = None,
            network: str = None,
            lifetime: int = 60,
            fee_paid_by_payer: float = None,
            under_paid_coverage: float = None,
            to_currency: str = None,
            auto_withdrawal: bool = False,
            email: str = None,
            order_id: str = None,
            description: str = None,
            sandbox: bool = False
    ):
        """

        :param amount:
        :param pay_currency:
        :param callback_url:
        :param currency:
        :param network:
        :param lifetime:
        :param fee_paid_by_payer:
        :param under_paid_coverage:
        :param to_currency:
        :param auto_withdrawal:
        :param email:
        :param order_id:
        :param description:
        :param sandbox:
        :return:
        """
        payment_data = {
            'amount': amount,
            'pay_currency': pay_currency,
            'callback_url': callback_url,
            'currency': currency,
            'network': network,
            'lifetime': lifetime,
            'fee_paid_by_payer': fee_paid_by_payer,
            'under_paid_coverage': under_paid_coverage,
            'to_currency': to_currency,
            'auto_withdrawal': auto_withdrawal,
            'email': email,
            'order_id': order_id,
            'description': description,
            'sandbox': sandbox,
        }
        try:
            return self._client.request('POST', 'payment/white-label', json_data=payment_data)
        except Exception:
            raise Exception

    def create_static_address(
            self,
            network: str,
            to_currency: str = None,
            auto_withdrawal: bool = False,
            callback_url: str = None,
            email: str = None,
            order_id: str = None,
            description: str = None,
    ):
        """

        :param network:
        :param to_currency:
        :param auto_withdrawal:
        :param callback_url:
        :param email:
        :param order_id:
        :param description:
        :return:
        """
        static_address_data = {
            'network': network,
        }

        if to_currency is not None:
            static_address_data['to_currency'] = to_currency
        if auto_withdrawal is not None:
            static_address_data['auto_withdrawal'] = auto_withdrawal
        if callback_url is not None:
            static_address_data['callback_url'] = callback_url
        if email is not None:
            static_address_data['email'] = email
        if order_id is not None:
            static_address_data['order_id'] = order_id
        if description is not None:
            static_address_data['description'] = description

        try:
            return self._client.request('POST', 'payment/static-address', json_data=static_address_data)
        except Exception:
            raise Exception

    def revoke_static_wallet(self, address: str):
        """
        Revokes a static wallet by disabling further transactions to the specified address.

        :param address: The address of the static wallet to revoke.
        :return: The result of the revocation process.
        """
        data = {
            'address': address
        }
        try:
            return self._client.request('POST', 'payment/static-address/revoke', json_data=data)
        except Exception:
            raise Exception

    def get_static_address_list(self):
        """

        :return:
        """
        try:
            return self._client.request('GET', 'payment/static-address')
        except Exception:
            raise Exception

    def get_payment_history(
            self,
            track_id: int = None,
            type_: str = None,
            status: str = None,
            pay_currency: str = None,
            currency: str = None,
            network: str = None,
            address: str = None,
            from_date: int = None,
            to_date: int = None,
            from_amount: float = None,
            to_amount: float = None,
            sort_by: str = 'create_date',
            sort_type: str = 'desc',
            page: int = 1,
            size: int = 10,
    ):
        """
        Retrieves the payment history based on specified filters.

        :param track_id: Filter payments by a specific invoice ID. Defaults to None.
        :param type_: Filter payments by type (e.g., 'Invoice', 'White-Label', 'Static Wallet'). Defaults to None.
        :param status: Filter payments by status (e.g., 'Paid', 'Confirming'). Defaults to None.
        :param pay_currency: Filter payments by a specific crypto currency symbol in which the pay amount is specified. Defaults to None.
        :param currency: Filter payments by a specific currency symbol. Defaults to None.
        :param network: Filter payments by the expected blockchain network for the specified crypto currency. Defaults to None.
        :param address: Filter payments by the expected address. It’s better to filter static addresses. Defaults to None.
        :param from_date: The start of the date window to query for payments in Unix format. Defaults to None.
        :param to_date: The end of the date window to query for payments in Unix format. Defaults to None.
        :param from_amount: Filter payments with amounts greater than or equal to the specified value. Defaults to None.
        :param to_amount: Filter payments with amounts less than or equal to the specified value. Defaults to None.
        :param sort_by: Sort the received list by a parameter. Possible values: 'create_date', 'pay_date', 'amount'. Default: 'create_date'.
        :param sort_type: Display the list in ascending or descending order. Possible values: 'asc', 'desc'. Default: 'desc'.
        :param page: The page number of the results to retrieve. Possible values: from 1 to the total number of pages. Default: 1.
        :param size: Number of records to display per page. Possible values: from 1 to 200. Default: 10.
        :return: The payment history.
        """
        data = {
            'track_id': track_id,
            'type': type_,
            'status': status,
            'pay_currency': pay_currency,
            'currency': currency,
            'network': network,
            'address': address,
            'from_date': from_date,
            'to_date': to_date,
            'from_amount': from_amount,
            'to_amount': to_amount,
            'sort_by': sort_by,
            'sort_type': sort_type,
            'page': page,
            'size': size,
        }

        query_params = {k: v for k, v in data.items() if v is not None}
        try:
            return self._client.request('GET', 'payment', query_params=query_params)
        except Exception:
            raise Exception

    def get_accepted_currencies(self):
        try:
            return self._client.request('GET', 'payment/accepted-currencies')
        except Exception:
            raise Exception

    def get_prices(self):
        try:
            return self._client.request('GET', 'common/prices')
        except Exception:
            raise Exception
