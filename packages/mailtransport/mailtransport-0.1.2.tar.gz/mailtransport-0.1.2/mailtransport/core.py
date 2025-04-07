from .mail import MailClient


class MailTransportClient(MailClient):
    """
    A client for interacting with the MailTransport API.
    """

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.mailtransportai.com/api/v1"
        self.mail_init = False
