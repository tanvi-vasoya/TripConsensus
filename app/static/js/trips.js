async function generateRecommendation(tripId) {

    const button = document.getElementById(
        "generate-btn",
    );

    button.disabled = true;
    button.innerText = "Generating AI Suggestions...";

    try {

        const response = await fetch(
            `/recommendations/${tripId}/generate`,
            {
                method: "POST",
            }
        );

        if (!response.ok) {

            const error = await response.text();

            throw new Error(error);

        }

        const recommendations = await response.json();

        const container = document.getElementById(
            "recommendation-container",
        );

        container.innerHTML = "";

        recommendations.forEach((recommendation) => {

            container.innerHTML += `

                <div class="card mt-3 border-success shadow-sm">

                    <div class="card-body">

                        <h4>

                            🏝 ${recommendation.destination}

                        </h4>

                        <p>

                            <strong>Estimated Cost:</strong>

                            ₹${recommendation.estimated_cost}

                        </p>

                        <p>

                            ${recommendation.reason}

                        </p>

                    </div>

                </div>

            `;

        });

        // Give the user a moment to see the suggestions
        button.innerText = "Redirecting to Voting...";

        setTimeout(() => {

            window.location.href =
                `/trip/${tripId}/vote`;

        }, 2000);

    }

    catch (error) {

        alert(error.message);

        button.disabled = false;

        button.innerText =
            "🤖 Generate AI Suggestions";

    }

}



// ===============================
// Survey Progress Bars
// ===============================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        document
            .querySelectorAll(".progress-bar")
            .forEach((bar) => {

                const progress =
                    bar.dataset.progress;

                if (progress) {

                    bar.style.width =
                        `${progress}%`;

                }

            });

    }
);