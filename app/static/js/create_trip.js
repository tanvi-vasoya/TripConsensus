const participantsContainer = document.getElementById("participants");

const addParticipantButton = document.getElementById("addParticipant");

let participantCount = 0;

addParticipantButton.addEventListener("click", () => {

    participantCount++;

    const card = document.createElement("div");

    card.className = "card shadow-sm mb-3 participant-card";

    card.innerHTML = `
        <div class="card-body">

            <div class="d-flex justify-content-between align-items-center mb-3">

                <h5 class="mb-0">
                    Participant #${participantCount}
                </h5>

                <button
                    type="button"
                    class="btn btn-sm btn-danger removeParticipant"
                >
                    Remove
                </button>

            </div>

            <div class="row">

                <div class="col-md-4">

                    <input
                        class="form-control participant-name"
                        placeholder="Name"
                    >

                </div>

                <div class="col-md-4">

                    <input
                        class="form-control participant-email"
                        placeholder="Email"
                    >

                </div>

                <div class="col-md-4">

                    <input
                        class="form-control participant-phone"
                        placeholder="+91..."
                    >

                </div>

            </div>

        </div>
    `;

    participantsContainer.appendChild(card);

    card
        .querySelector(".removeParticipant")
        .addEventListener("click", () => {

            card.remove();

        });

});

document
    .getElementById("tripForm")
    .addEventListener("submit", async (event) => {

        event.preventDefault();

        const participants = [];

        document
            .querySelectorAll(".participant-card")
            .forEach((card) => {

                participants.push({
                    name: card.querySelector(".participant-name").value,
                    email: card.querySelector(".participant-email").value,
                    phone_number: card.querySelector(".participant-phone").value,
                });

            });

        const payload = {

            title: document.getElementById("title").value,

            description: document.getElementById("description").value,

            organizer: {

                name: document.getElementById("organizerName").value,

                email: document.getElementById("organizerEmail").value,

                phone_number: document.getElementById("organizerPhone").value,

            },

            participants: participants,

        };

        console.log(payload);

        try {

            const response = await fetch("/trips", {

                method: "POST",

                headers: {

                    "Content-Type": "application/json",

                },

                body: JSON.stringify(payload),

            });

            if (!response.ok) {

                const error = await response.text();
                console.error(error);
                alert(error);
                return;

            }

            const trip = await response.json();

            window.location.href = `/trip/${trip.id}`;

        }

        catch (error) {

            console.error(error);

            alert("Unable to create trip.");

        }

    });