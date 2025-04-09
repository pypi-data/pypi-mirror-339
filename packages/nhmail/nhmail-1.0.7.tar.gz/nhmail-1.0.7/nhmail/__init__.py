from marshmallow import ValidationError

from nhmail.constants import LAMBDA_URI, ENDPOINT_FOR_SEND_EMAIL, LAMBDA_AUTHEN
from nhmail.client import ServiceHttpClient
from nhmail.validators import SendEmailSchema

HEADERS = {
    "Authorization": LAMBDA_AUTHEN,
    "Content-Type": "application/json",
}


class MailWrapSystem:
    def __init__(self, body: dict = None):
        self.body = body

    def _validate_body(self):
        """Validates the self.body against the SendEmailSchema."""
        if self.body is None:
            raise ValueError("Request body cannot be None.")
        try:
            SendEmailSchema().load(self.body)
        except ValidationError as err:
            raise ValueError(err.messages)

    def _send_email(self):
        """Sends the email using the ServiceHttpClient."""
        response = ServiceHttpClient(base_url=LAMBDA_URI).execute(
            method="post",
            uri=ENDPOINT_FOR_SEND_EMAIL,
            body=self.body,
            headers=HEADERS,
        )
        return response.get("body")

    def send_verify_password(self):
        self._validate_body()
        return self._send_email()

    def send_welcome(self):
        self._validate_body()
        return self._send_email()

    def send_staff_confirm(self):
        self._validate_body()
        return self._send_email()

    def send_custom_body(self):
        # No validation for custom body in this version
        return self._send_email()
