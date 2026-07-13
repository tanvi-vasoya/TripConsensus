from app.models.participant import Participant
from app.models.trip import Trip
from app.sms.survey_flow import SurveyFlow
from app.sms.twilio_client import TwilioClient


class SMSService:
    """
    Service responsible for sending SMS messages.
    """

    def __init__(
        self,
        client: TwilioClient,
    ) -> None:

        self.client = client

    def send_sms(
        self,
        phone_number: str,
        message: str,
    ) -> str:
        """
        Send an SMS message.
        """
        print("=" * 80)
        print("SMSService.send_sms() CALLED")
        print("TO:", phone_number)
        print("MESSAGE:", message)
        print("=" * 80)

        return self.client.send_sms(
            to=phone_number,
            body=message,
        )

    def send_trip_invitation(
        self,
        participant: Participant,
        trip: Trip,
    ) -> str:
        """
        Send the initial trip invitation.
        """

        return self.send_sms(
            participant.phone_number,
            SurveyFlow.invitation_message(
                participant,
                trip,
            ),
        )

    def send_survey_reminder(
        self,
        participant: Participant,
        trip: Trip,
    ) -> str:
        """
        Send a reminder to complete the survey.
        """

        return self.send_sms(
            participant.phone_number,
            SurveyFlow.reminder_message(
                participant,
                trip,
            ),
        )

    def send_thank_you(
        self,
        participant: Participant,
    ) -> str:
        """
        Send a thank-you message.
        """

        return self.send_sms(
            participant.phone_number,
            SurveyFlow.thank_you_message(
                participant,
            ),
        )

    def send_voting_invitation(
        self,
        participant: Participant,
        trip: Trip,
    ) -> str:
        """
        Send the voting invitation.
        """

        return self.send_sms(
            participant.phone_number,
            SurveyFlow.voting_message(
                participant,
                trip,
            ),
        )