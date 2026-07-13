from enum import Enum


class TripStatus(str, Enum):
    """
    Lifecycle states of a trip.
    """

    PLANNING = "planning"
    SURVEY = "survey"
    RECOMMENDATIONS = "recommendations"
    VOTING = "voting"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"