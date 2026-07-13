const tripId = window.location.pathname.split("/")[2];

let participants = [];
let recommendations = [];

document.addEventListener(
    "DOMContentLoaded",
    loadPage,
);

async function loadPage() {

    await loadParticipants();

    await loadRecommendations();

    document
        .getElementById("submit-vote")
        .addEventListener(
            "click",
            submitVotes,
        );

}

async function loadParticipants() {

    const response = await fetch(
        `/trips/${tripId}`
    );

    const trip = await response.json();

    participants = trip.participants;

    const select = document.getElementById(
        "participant-select",
    );

    participants.forEach((participant) => {

        select.innerHTML += `
            <option value="${participant.id}">
                ${participant.name}
            </option>
        `;

    });

}

async function loadRecommendations() {

    const response = await fetch(
        `/recommendations/${tripId}`
    );

    recommendations = await response.json();

    const container = document.getElementById(
        "recommendation-list",
    );

    container.innerHTML = "";

    recommendations.forEach((recommendation) => {

        container.innerHTML += `

        <div class="card mb-3">

            <div class="card-body">

                <h4>

                    📍 ${recommendation.destination}

                </h4>

                <p>

                    <strong>Estimated Cost:</strong>

                    ₹${recommendation.estimated_cost}

                </p>

                <p>

                    ${recommendation.reason}

                </p>

                <label>

                    Rank

                </label>

                <select
                    class="form-select rank-select"
                    data-id="${recommendation.id}"
                >

                    <option value="">
                        Select Rank
                    </option>

                    <option value="1">
                        🥇 First Choice
                    </option>

                    <option value="2">
                        🥈 Second Choice
                    </option>

                    <option value="3">
                        🥉 Third Choice
                    </option>

                </select>

            </div>

        </div>

        `;

    });

}

async function submitVotes() {

    const participantId = document.getElementById(
        "participant-select",
    ).value;

    if (!participantId) {

        alert("Please select yourself.");

        return;

    }

    const submitButton = document.getElementById(
        "submit-vote",
    );

    const selects = document.querySelectorAll(
        ".rank-select",
    );

    const usedRanks = new Set();

    for (const select of selects) {

        if (!select.value) {

            alert(
                "Please rank every destination."
            );

            return;

        }

        if (usedRanks.has(select.value)) {

            alert(
                "Duplicate ranks are not allowed."
            );

            return;

        }

        usedRanks.add(
            select.value,
        );

    }

    submitButton.disabled = true;
    submitButton.innerText = "Submitting Votes...";

    try {

        for (const select of selects) {

            const response = await fetch(
                "/votes",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json",
                    },

                    body: JSON.stringify({

                        participant_id:
                            participantId,

                        recommendation_id:
                            select.dataset.id,

                        rank:
                            Number(select.value),

                    }),

                },
            );

            if (!response.ok) {

                throw new Error(
                    "Failed to submit vote."
                );

            }

        }

        submitButton.innerText =
            "Redirecting...";

        alert(
            "🎉 Vote submitted successfully!"
        );

        setTimeout(() => {

            window.location.href =
                `/trip/${tripId}/suggested-trip`;

        }, 1500);

    }

    catch (error) {

        alert(
            error.message ||
            "Unable to submit votes."
        );

        submitButton.disabled = false;

        submitButton.innerText =
            "Submit Vote";

    }

}