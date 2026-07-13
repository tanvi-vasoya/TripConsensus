from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from app.config import settings


class TwilioClient:
    """
    Wrapper around the Twilio SDK.

    This class isolates all Twilio-specific logic from the
    rest of the application.
    """

    def __init__(self) -> None:

        self.client = Client(
            settings.twilio_account_sid,
            settings.twilio_auth_token,
        )

        self.from_number = settings.twilio_phone_number

    def send_sms(
        self,
        to: str,
        body: str,
    ) -> str:
        """
        Send an SMS message.

        Returns:
            Twilio Message SID.
        """

        print("=" * 80)
        print("TwilioClient.send_sms() CALLED")
        print("TO:", to)
        print("FROM:", self.from_number)
        print("=" * 80)


        # ---------------------------------------------------
        # DEVELOPMENT MODE
        # ---------------------------------------------------

        if not settings.enable_sms:

            print("\n" + "=" * 80)
            print("📱 MOCK SMS")
            print("=" * 80)
            print(f"To      : {to}")
            print(f"From    : {self.from_number}")
            print("-" * 80)
            print(body)
            print("=" * 80 + "\n")

            return "mock-message-sid"

        # ---------------------------------------------------
        # PRODUCTION MODE
        # ---------------------------------------------------

        try:
            
            print("Calling Twilio API...")
            message = self.client.messages.create(
                body=body,
                from_=self.from_number,
                to=to,
            )

            return message.sid

        except TwilioRestException:
            raise

    def health_check(
        self,
    ) -> bool:
        """
        Verify that Twilio credentials are valid.
        """

        try:

            self.client.api.accounts(
                settings.twilio_account_sid,
            ).fetch()

            return True

        except Exception:

            return False