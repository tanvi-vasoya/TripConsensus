from app.models.participant import Participant
from app.models.trip import Trip


class SurveyFlow:
    """
    Generates SMS messages used throughout the survey workflow.
    """

    @staticmethod
    def invitation_message(
        participant: Participant,
        trip: Trip,
    ) -> str:
        """
        Generate the initial survey invitation.
        """

        survey_link = (
            f"http://localhost:8000/survey/{participant.id}"
        )

        return (
            f"Hi {participant.name},\n\n"
            f"You've been invited to join the trip "
            f"'{trip.title}'.\n\n"
            f"Please complete your travel preferences survey:\n"
            f"{survey_link}\n\n"
            f"Thank you!"
        )

    @staticmethod
    def reminder_message(
        participant: Participant,
        trip: Trip,
    ) -> str:
        """
        Generate a reminder message.
        """

        survey_link = (
            f"http://localhost:8000/survey/{participant.id}"
        )

        return (
            f"Hi {participant.name},\n\n"
            f"This is a reminder to complete your survey "
            f"for '{trip.title}'.\n\n"
            f"{survey_link}"
        )

    @staticmethod
    def thank_you_message(
        participant: Participant,
    ) -> str:
        """
        Generate a thank-you message.
        """

        return (
            f"Thanks {participant.name}! 🎉\n\n"
            f"We've received your travel preferences."
        )

    @staticmethod
    def voting_message(
        participant: Participant,
        trip: Trip,
    ) -> str:
        """
        Generate the voting invitation.
        """

        voting_link = (
            f"http://localhost:8000/vote/{trip.id}"
        )

        return (
            f"Hi {participant.name},\n\n"
            f"Your group's AI recommendations are ready!\n\n"
            f"Please rank your favorite destinations:\n"
            f"{voting_link}"
        )