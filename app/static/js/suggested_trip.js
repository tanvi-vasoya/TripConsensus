const tripId = window.location.pathname.split("/")[2];

loadSuggestedTrip();

async function loadSuggestedTrip() {

    const result = await fetch(
        `/votes/results/${tripId}`
    );

    const data = await result.json();

    const recommendations = await fetch(
        `/recommendations/${tripId}`
    );

    const list = await recommendations.json();

    const recommendation = list.find(

        r => r.destination === data.winner

    );

    const container = document.getElementById(
        "suggested-trip-container"
    );

    if (!recommendation) {

        container.innerHTML = `
            <div class="card-body">

                <h3>

                    No suggested trip available.

                </h3>

            </div>
        `;

        return;

    }

    container.innerHTML = `

        <div class="card-body">

            <h2>

                📍 ${recommendation.destination}

            </h2>

            <hr>

            <p>

                <strong>Estimated Cost</strong>

                ₹${recommendation.estimated_cost}

            </p>

            <p>

                ${recommendation.reason}

            </p>

            <hr>

            <p class="text-muted">

                Suggested using AI recommendations
                and Group Ranked Choice Voting.

            </p>

        </div>

    `;

}