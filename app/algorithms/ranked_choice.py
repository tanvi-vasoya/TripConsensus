from __future__ import annotations

from dataclasses import dataclass
from collections import Counter

@dataclass
class Ballot:
    """
    Represents a participant's ranked preferences.
    """

    preferences: list[str]

    def first_choice(
        self,
    ) -> str | None:
        """
        Return the participant's highest-ranked remaining choice.
        """

        if not self.preferences:
            return None

        return self.preferences[0]

    def remove_candidate(
        self,
        candidate: str,
    ) -> None:
        """
        Remove an eliminated candidate from the ballot.
        """

        self.preferences = [
            preference
            for preference in self.preferences
            if preference != candidate
        ]


class RankedChoiceVoting:
    """
    Ranked Choice Voting (Instant Runoff Voting).
    """

    def __init__(
        self,
        ballots: list[Ballot],
    ) -> None:

        self.ballots = ballots


    def count_first_choices(
        self,
    ) -> Counter[str]:
        """
        Count the first-choice vote for every ballot.
        """

        counts: Counter[str] = Counter()

        for ballot in self.ballots:

            first_choice = ballot.first_choice()

            if first_choice is None:
                continue

            counts[first_choice] += 1

        return counts
    

    def has_majority(
        self,
        counts: Counter[str],
    ) -> str | None:
        """
        Return the winning candidate if someone has a majority.
        """

        total_votes = sum(
            counts.values(),
        )

        if total_votes == 0:
            return None

        majority = total_votes / 2

        for candidate, votes in counts.items():

            if votes > majority:

                return candidate

        return None
    

    def eliminate_lowest(
        self,
        counts: Counter[str],
    ) -> str:
        """
        Eliminate the candidate with the fewest first-choice votes.

        Returns:
            Name of the eliminated candidate.
        """

        lowest_candidate = min(
            counts,
            key=counts.get,
        )

        for ballot in self.ballots:

            ballot.remove_candidate(
                lowest_candidate,
            )

        return lowest_candidate
    

    def is_tie(
        self,
        counts: Counter[str],
    ) -> bool:
        """
        Return True if every remaining candidate has
        the same number of votes.
        """

        if not counts:
            return True

        return len(
            set(counts.values())
        ) == 1
    

    def run(
        self,
    ) -> str | None:
        """
        Execute the Ranked Choice Voting election.

        Returns:
            The winning candidate or None if the election ends in a tie.
        """

        while True:

            counts = self.count_first_choices()

            winner = self.has_majority(
                counts,
            )

            if winner is not None:

                return winner

            if self.is_tie(
                counts,
            ):

                return None

            self.eliminate_lowest(
                counts,
            )