import requests

from requests.models import Response

from typing import Optional

class MyFatoorah:
    def __init__(self, base_url: str, api_token: str):
        self.base_url: str = base_url
        self.api_token: str = api_token
        self.headers: str = {
            'Authorization': 'Bearer {}'.format(self.api_token)
        }
    

    def send_request(self, api_url: str, payload: dict) -> Response:
        return requests.post(api_url, json=payload, headers=self.headers)
    

    def initiate_payment(self, invoice_amount: float, currency_iso: str) -> Response:
        payload: dict = {
            'InvoiceAmount': invoice_amount,
            'CurrencyIso': currency_iso
        }

        return self.send_request(self.base_url + 'InitiatePayment', payload)


    def initiate_session(self, customer_id: str, save_token: str=False) -> Response:
        payload: dict = {
            'CustomerIdentifier': customer_id
        }
        
        if save_token:
            payload['SaveToken'] = save_token

        return self.send_request(self.base_url + 'InitiateSession', payload)
    

    def execute_payment(self, invoice_value: float, session_id: Optional[str]=None, payment_method_id: Optional[int]=None, display_currency_iso: str=None, callback_url: str=None) -> Response:
        if all([session_id is None, payment_method_id is None]):
            raise Exception('Either payment_method_id or session_id is required')

        payload: dict = {
            "InvoiceValue": invoice_value
        }

        if session_id is not None:
            payload['SessionId'] = session_id
        
        else:
            payload['PaymentMethodId'] = payment_method_id

        if callback_url is not None:
            payload['CallBackUrl'] = callback_url

        if display_currency_iso is not None:
            payload['DisplayCurrencyIso'] = display_currency_iso

        return self.send_request(self.base_url + 'ExecutePayment', payload)

    def make_refund(self, key_type: str, key: str, service_charge_on_customer: bool, amount: float, comment: str, amount_deducted_from_supplier: Optional[float]=None) -> Response:
        payload: dict = {
            'KeyType': key_type,
            'Key': key,
            'ServiceChargeOnCustomer': service_charge_on_customer,
            'Amount': amount,
            'Comment': comment
        }

        if amount_deducted_from_supplier:
            payload['AmountDeductedFromSupplier'] = amount_deducted_from_supplier

        return self.send_request(self.base_url + 'MakeRefund', payload)

    def get_payment_status(self, key_type: str, key: str) -> Response:
        payload: dict = {
            'Key': key,
            'KeyType': key_type
        }
        return self.send_request(self.base_url + 'GetPaymentStatus', payload)
    
    def get_payment_status_by_payment_id(self, payment_id: str) -> Response:
        return self.get_payment_status('PaymentId', payment_id)
    
    def get_payment_status_by_invoice_id(self, invoice_id: str) -> Response:
        return self.get_payment_status('InvoiceId', invoice_id)