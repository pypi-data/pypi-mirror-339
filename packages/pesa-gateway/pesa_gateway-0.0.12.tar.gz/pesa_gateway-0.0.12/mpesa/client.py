import time
import base64
from requests.auth import HTTPBasicAuth
from typing import Optional, Callable, Dict, Any
from mpesa.config import MpesaConfig
from mpesa.utils import Utility


class Decorators:
    """
    A utility class containing decorator methods for the M-Pesa client.
    """

    @staticmethod
    def refresh_token(decorated: Callable) -> Callable:
        """
        A decorator that automatically refreshes the OAuth access token if expired.

        This decorator checks if the current access token has expired before executing
        the decorated method. If expired, it obtains a new access token by calling
        get_access_token().

        Args:
            decorated (Callable): The method being decorated

        Returns:
            Callable: A wrapper function that handles token refresh
        """

        def wrapper(gateway, *args, **kwargs):
            if (
                gateway.access_token_expiration
                and time.time() > gateway.access_token_expiration
            ):
                gateway.access_token = gateway.get_access_token()
            return decorated(gateway, *args, **kwargs)

        return wrapper


class MpesaClient:
    """
    Client class for interacting with the M-Pesa API.

    This class provides methods for making various M-Pesa API calls including:
    - STK Push requests
    - Account balance queries
    - Business-to-Business (B2B) payments
    - Business-to-Customer (B2C) payments
    - QR code generation
    - Express checkout
    - Business buy goods transactions

    Args:
        config (Optional[MpesaConfig]): Configuration object containing API credentials and settings.
            If not provided, will create a new MpesaConfig instance with default values.

    Attributes:
        config (MpesaConfig): The configuration object used by this client
        headers (dict): HTTP headers including the OAuth bearer token
        password (str): Base64 encoded password for API authentication
        timestamp (str): Current timestamp used for API requests
        access_token_expiration (float): Unix timestamp when the current access token expires
    """

    def __init__(self, config: Optional[MpesaConfig] = None):
        self.config = config or MpesaConfig()
        self.headers = {"Authorization": f"Bearer {self.get_access_token()}"}
        self.password = self.generate_password()

    def get_headers(self) -> dict:
        """
        Get the basic authentication headers for API requests.

        Returns:
            dict: Headers dictionary containing the Basic auth credentials
        """
        return {
            "Authorization": f"Basic {HTTPBasicAuth(self.config.consumer_key, self.config.consumer_secret)}"
        }

    def generate_password(self) -> str:
        """
        Generate the base64 encoded password required for M-Pesa API authentication.

        Returns:
            str: Base64 encoded password string
        """
        self.timestamp = time.strftime("%Y%m%d%H%M%S")
        password = f"{self.config.shortcode}{self.config.passkey}{self.timestamp}"
        password_bytes = password.encode("utf-8")
        return base64.b64encode(password_bytes).decode("utf-8")

    def generate_security_credential(self) -> str:
        """
        Generate the security credential required for M-Pesa API authentication.

        Returns:
            str: Security credential string
        """
        encoded_string = base64.b64encode(
            f"{self.config.shortcode}{self.config.passkey}".encode("utf-8")
        ).decode("utf-8")
        # encrypt the encoded string
        encrypted_string = Utility.encrypt_string(
            encoded_string, self.config.consumer_key
        )
        return encrypted_string

    def get_access_token(self) -> str:
        """
        Get an OAuth access token from the M-Pesa API.

        Returns:
            str: The access token string

        Raises:
            Exception: If the request times out or connection fails
            ValueError: If the response doesn't contain an access token
        """
        url = f"{self.config.base_url}/oauth/v1/generate?grant_type=client_credentials"

        token_data = Utility.make_request(
            "get",
            url,
            auth=HTTPBasicAuth(self.config.consumer_key, self.config.consumer_secret),
        )["response"]

        if "access_token" not in token_data:
            raise ValueError("Access token not found in response")

        # Store token expiration time (typically 1 hour)
        self.access_token_expiration = time.time() + 3600

        return token_data["access_token"]

    @Decorators.refresh_token
    def stk_push_request(self, data: dict) -> Dict[str, Any]:
        """
        Initiates an STK push request to the M-Pesa API.

        Args:
            data (dict): A dictionary containing:
                - amount (str): The amount to be charged
                - phone_number (str): The phone number to be charged
                - account_reference (str): The account reference
                - transaction_description (str): Description of the transaction

        Returns:
            JSON: The response from the M-Pesa API
        """

        url = f"{self.config.base_url}/mpesa/stkpush/v1/processrequest"

        payload = {
            "BusinessShortCode": self.config.shortcode,
            "Password": self.password,
            "Timestamp": self.timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": data["amount"],
            "PartyA": data["phone_number"],
            "PartyB": self.config.shortcode,
            "PhoneNumber": data["phone_number"],
            "CallBackURL": self.config.callback_url,
            "AccountReference": data["account_reference"],
            "TransactionDesc": data["transaction_description"],
            "headers": self.headers,
        }

        return Utility.make_request("post", url, headers=self.headers, json=payload)

    @Decorators.refresh_token
    def account_balance(self, data: dict) -> Dict[str, Any]:
        """
        Queries the account balance for the configured shortcode.

        Args:
            data (dict): A dictionary containing:
                - remarks (str): Comments that are sent along with the transaction
                - initiator (str): The name of the initiator initiating the request
                - security_credential (str): The security credential of the initiator
                - queue_timeout_url (str): The URL to be specified in case of a timeout
                - result_url (str): The URL that will receive the response

        Returns:
            JSON: The response from the M-Pesa API containing account balance information
        """

        url = f"{self.config.base_url}/mpesa/accountbalance/v1/query"
        payload = {
            "Initiator": data["initiator"],
            "SecurityCredential": self.generate_security_credential(),
            "CommandID": "AccountBalance",
            "PartyA": self.config.shortcode,
            "IdentifierType": "4",
            "Remarks": data["remarks"],
            "QueueTimeOutURL": data["queue_timeout_url"],
            "ResultURL": data["result_url"],
        }
        print(payload)
        print(self.headers)
        print(url)
        return Utility.make_request("post", url, headers=self.headers, json=payload)

    @Decorators.refresh_token
    def business_to_business_payment(self, data: dict) -> Dict[str, Any]:
        """
        Initiates a business-to-business (B2B) payment transaction.

        This method allows a business to make payments to another business through the M-Pesa API.

        Args:
            data (dict): A dictionary containing:
                - initiator (str): The name of the initiator initiating the request
                - security_credential (str): The security credential of the initiator
                - amount (str): The amount to be transacted
                - party_a (str): The organization sending the transaction
                - party_b (str): The organization receiving the funds
                - account_reference (str): Account reference for the transaction
                - requester (str): The phone number of the requesting party
                - remarks (str): Comments that are sent along with the transaction
                - queue_timeout_url (str): The URL to be specified in case of a timeout
                - result_url (str): The URL that will receive the response
                - occassion (str): Optional parameter for additional transaction information

        Returns:
            JSON: The response from the M-Pesa API containing B2B payment information
        """
        url = f"{self.config.base_url}/mpesa/b2b/v1/paymentrequest"
        payload = {
            "Initiator": data["initiator"],
            "SecurityCredential": self.generate_security_credential(),
            "CommandID": "BusinessPayBill",
            "SenderIdentifierType": "4",
            "RecieverIdentifierType": "4",
            "Amount": data["amount"],
            "PartyA": data["party_a"],
            "PartyB": data["party_b"],
            "AccountReference": data["account_reference"],
            "Requester": data["requester"],
            "Remarks": data["remarks"],
            "QueueTimeOutURL": data["queue_timeout_url"],
            "ResultURL": data["result_url"],
            "Occassion": data["occassion"],
        }
        return Utility.make_request("post", url, headers=self.headers, json=payload)

    @Decorators.refresh_token
    def b2b_express_checkout(self, data: dict) -> Dict[str, Any]:
        """
        Initiates a B2B express checkout transaction.

        This method enables merchants to initiate USSD Push to till enabling their fellow merchants to pay from their own till numbers to the vendors paybill.

        Args:
            data (dict): A dictionary containing:
                - primary_short_code (str): The shortcode of the primary party
                - receiver_short_code (str): The shortcode of the receiver party
                - amount (str): The amount to be transacted
                - payment_ref (str): The reference for the payment
                - callback_url (str): The URL to be specified in case of a timeout
                - partner_name (str): The name of the partner
                - request_ref_id (str): The reference for the request

        Returns:
            JSON: The response from the M-Pesa API containing B2B express checkout information
        """

        url = f"{self.config.base_url}/v1/ussdpush/get-msisdn"
        payload = {
            "primaryShortCode": data["primary_short_code"],
            "receiverShortCode": data["receiver_short_code"],
            "amount": data["amount"],
            "paymentRef": data["payment_ref"],
            "callbackUrl": data["callback_url"],
            "partnerName": data["partner_name"],
            "RequestRefID": data["request_ref_id"],
        }
        return Utility.make_request("post", url, headers=self.headers, json=payload)

    @Decorators.refresh_token
    def generate_dynamic_qr_code(self, data: dict) -> Dict[str, Any]:
        """
        Generates a dynamic QR code for M-Pesa payments.

        This method creates a QR code that can be scanned by customers to make payments
        through M-Pesa. The QR code contains payment information such as merchant name,
        amount, and transaction details.

        Args:
            data (dict): A dictionary containing:
                - merchant_name (str): The name of the merchant receiving payment
                - ref_no (str): Reference number for the transaction
                - amount (str): The amount to be paid
                - trx_code (str): Transaction code defining the type of transaction
                - cpi (str): Credit Party Identifier
                - size (str): Size of the QR code to be generated

        Returns:
            JSON: The response from the M-Pesa API containing the generated QR code data
        """
        url = f"{self.config.base_url}/mpesa/qrcode/v1/generate"
        payload = {
            "MerchantName": data["merchant_name"],
            "RefNo": data["ref_no"],
            "Amount": data["amount"],
            "TrxCode": data["trx_code"],
            "CPI": data["cpi"],
            "Size": data["size"],
        }
        return Utility.make_request("post", url, headers=self.headers, json=payload)

    @Decorators.refresh_token
    def business_to_customer_payment(self, data: dict) -> Dict[str, Any]:
        """
        Initiates a Business-to-Customer (B2C) payment transaction.

        This method allows businesses to make payments to customers by transferring
        funds from a business account to a customer's M-Pesa account.

        Args:
            data (dict): A dictionary containing:
                - initiator_name (str): Name of the initiator initiating the request
                - security_credential (str): Security credential for the initiator
                - amount (str): The amount to be transferred to the customer
                - party_a (str): Organization's shortcode initiating the transaction
                - party_b (str): Phone number of the customer receiving the amount
                - remarks (str): Comments about the transaction
                - queue_timeout_url (str): URL to send timeout notification
                - result_url (str): URL to send successful transaction notification
                - occasion (str): Optional description of the occasion

        Returns:
            JSON: The response from the M-Pesa API containing B2C payment information
        """
        url = f"{self.config.base_url}/mpesa/b2c/v1/paymentrequest"
        payload = {
            "InitiatorName": data["initiator_name"],
            "SecurityCredential": data["security_credential"],
            "CommandID": "BusinessPayment",
            "Amount": data["amount"],
            "PartyA": data["party_a"],
            "PartyB": data["party_b"],
            "Remarks": data["remarks"],
            "QueueTimeOutURL": data["queue_timeout_url"],
            "ResultURL": data["result_url"],
            "Occasion": data["occasion"],
        }
        return Utility.make_request("post", url, headers=self.headers, json=payload)

    @Decorators.refresh_token
    def business_buy_goods(self, data: dict) -> Dict[str, Any]:
        """
        Initiates a Business Buy Goods transaction.

        This method enables you to pay for goods and services directly from your business account to a till number, merchant store number or Merchant HO.

        Args:
            data (dict): A dictionary containing:
                - initiator (str): The name of the initiator initiating the request
                - security_credential (str): The security credential of the initiator
                - amount (str): The amount to be transacted
                - party_a (str): The organization sending the transaction
                - party_b (str): The organization receiving the funds
                - account_reference (str): The account reference for the transaction
                - requester (str): The phone number of the requesting party
                - remarks (str): Comments about the transaction
                - queue_timeout_url (str): URL to send timeout notification
                - result_url (str): URL to send successful transaction notification

        Returns:
            JSON: The response from the M-Pesa API containing B2B express checkout information
        """
        url = f"{self.config.base_url}/mpesa/b2c/v1/paymentrequest"
        payload = {
            "Initiator": data["initiator"],
            "SecurityCredential": data["security_credential"],
            "Command ID": "BusinessBuyGoods",
            "SenderIdentifierType": "4",
            "RecieverIdentifierType": "4",
            "Amount": data["amount"],
            "PartyA": data["party_a"],
            "PartyB": data["party_b"],
            "AccountReference": data["account_reference"],
            "Requester": data["requester"],
            "Remarks": data["remarks"],
            "QueueTimeOutURL": data["queue_timeout_url"],
            "ResultURL": data["result_url"],
        }
        return Utility.make_request("post", url, headers=self.headers, json=payload)
