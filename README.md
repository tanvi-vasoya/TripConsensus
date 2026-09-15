# TripConsensus

TripConsensus is an end-to-end group trip planning web application. It collects each participant's travel preferences via SMS (and a web form), generates AI-based destination recommendations from those preferences using a fine-tuned Llama 3.1 model served through Ollama, and lets the group pick a final destination using Ranked-Choice Voting.

**Tech stack:** FastAPI (backend framework), Pydantic (schema validation), SQLAlchemy (ORM), PostgreSQL (database), Twilio Python SDK (SMS), Ollama (LLM inference — fine-tuned Llama 3.1).

The project follows a layered architecture: **Schemas → Models → Repositories → Services → API → Main**, described below in that order.

---

## 1. `app/schemas/`

Pydantic schemas used for request validation and response serialization at the API boundary. These do not touch the database directly — they define what a client can send in and what the API sends back.

- **`participant.py`** — `ParticipantCreate`, `ParticipantUpdate`, `ParticipantResponse`. Validates participant name, E.164-formatted phone number, and optional email.
- **`trip.py`** — `TripCreate`, `TripUpdate`, `TripResponse`. Defines a trip's title/description, its organizer, and its list of participants.
- **`survey_response.py`** — `SurveyResponseCreate`, `SurveyResponseUpdate`, `SurveyResponseResponse`. Captures budget, date availability, and preference lists (climate, activities, food, transport, accommodation), with a validator ensuring `available_from <= available_to`.
- **`recommendation.py`** — `RecommendationCreate`, `RecommendationUpdate`, `RecommendationResponse`. Represents an AI-generated destination suggestion, including cost estimate, confidence score, and which model/prompt version produced it.
- **`vote.py`** — `VoteCreate`, `VoteUpdate`, `VoteResponse`, `VotingResultResponse`. Represents a single ranked vote from a participant for a recommendation, and the final winner of an election.

## 2. `app/models/`

SQLAlchemy ORM classes. Each class maps to one PostgreSQL table and is created automatically on app startup.

- **`trip.py`** — `Trip` table: title, description, final agreed dates, status (`TripStatus` enum), and relationships to participants, recommendations, and model usage records.
- **`participant.py`** — `Participant` table: name, phone number, email, organizer flag, survey-completion flag, and current SMS survey question index. Related to a trip, its survey response, and its votes.
- **`survey_response.py`** — `SurveyResponse` table: one participant's submitted preferences (budget, availability, climate/activity/food/transport/accommodation preferences stored as JSON lists).
- **`recommendation.py`** — `Recommendation` table: one AI-generated destination suggestion for a trip, along with the model provider/name/prompt version used to generate it.
- **`vote.py`** — `Vote` table: a participant's rank for a specific recommendation.
- **`model_usage.py`** — `ModelUsage` table: logs AI usage per trip (provider, model, prompt version, token counts, response time, estimated cost).
- **`enums.py`** — `TripStatus` enum: the lifecycle stages a trip moves through (`planning`, `survey`, `recommendations`, `voting`, `confirmed`, `completed`).

## 3. `app/repositories/`

The data-access layer. Each repository wraps direct SQLAlchemy queries for one model and exposes CRUD plus a few targeted lookup methods. No business logic lives here — only database reads/writes.

- **`trip_repository.py`** — create/get/update/delete a trip; also `get_by_status` and `search_by_title`.
- **`participant_repository.py`** — create/get/update/delete a participant; also `get_by_trip_id`, `get_organizers`, `get_by_phone_number`, `search_by_name`.
- **`survey_repository.py`** — create/get/update/delete a survey response; also `get_by_participant_id`, `get_by_trip_id`, `get_by_budget_range`, `get_submitted_between`, `search_by_activity`.
- **`recommendation_repository.py`** — create/get/update/delete a recommendation; also `get_by_trip_id`, `get_by_model`, `get_by_prompt_version`, `delete_by_trip_id`, `get_best_recommendation` (highest confidence score).
- **`vote_repository.py`** — create/get/update/delete a vote; also `get_by_participant_id`, `get_by_recommendation_id`, `get_by_participant_and_recommendation`, `get_ranked_votes`.
- **`model_usage_repository.py`** — create/get/update/delete a usage record; also `get_by_trip_id`, `get_by_provider`, `get_by_model`, `get_by_prompt_version`, `get_total_estimated_cost`.

## 4. `app/services/`

The business-logic layer. Services combine one or more repositories (and other services) to carry out an actual workflow. This is where things like validation rules, orchestration across tables, and calls to Twilio/the AI model happen.

- **`trip_service.py`** — creates a trip along with its organizer and invited participants in a single transaction, then sends each of them an SMS invitation. Also handles fetching, updating, and deleting trips and reading a trip's organizer/participants.
- **`survey_service.py`** — drives the SMS-based survey flow: starts the survey for a participant, processes each incoming SMS answer against `SurveyEngine`, validates it, saves it to the participant's `SurveyResponse` field by field, advances to the next question, and sends a thank-you message once complete.
- **`web_survey_service.py`** — handles the same survey, but submitted in one shot through the web form instead of question-by-question over SMS.
- **`sms_service.py`** — thin wrapper around the Twilio client that sends trip invitations, survey reminders, thank-you messages, and voting invitations.
- **`recommendation_service.py`** — loads a trip and its collected survey responses, renders a prompt, sends it to the AI gateway (Ollama), parses the model's response into structured recommendations, and saves them (replacing any previous recommendations for that trip). Also exposes fetching and deleting recommendations.
- **`voting_service.py`** — records ranked votes (rejecting duplicate votes from the same participant for the same recommendation), retrieves votes, and determines the final winner by converting stored votes into ranked ballots and running them through the `RankedChoiceVoting` algorithm.

## 5. `app/api/`

FastAPI routers — the HTTP endpoints exposed by the application. Each file wires a service into one or more routes and translates errors into HTTP responses.

- **`trips.py`** (`/api/trips`) — `POST /` create a trip, `GET /` list all trips, `GET /{trip_id}` get one trip, `DELETE /{trip_id}` delete a trip.
- **`survey.py`** (`/survey/{participant_id}`) — `GET` renders the web survey form, `POST` validates and submits the answers via `WebSurveyService`.
- **`sms_webhook.py`** (`/sms/webhook`) — receives incoming SMS messages from Twilio (currently logs the payload; wiring it into `SurveyService.process_message` is a pending TODO in the code).
- **`recommendations.py`** (`/recommendations`) — `POST /{trip_id}/generate` triggers AI recommendation generation for a trip, `GET /{trip_id}` fetches existing recommendations.
- **`votes.py`** (`/votes`) — `POST /` cast a ranked vote, `GET /results/{trip_id}` get the IRV winner, `GET /{vote_id}` get one vote, `GET /recommendation/{recommendation_id}` get all votes for a recommendation, `DELETE /{vote_id}` delete a vote, `GET /` list all votes.

## 6. `app/main.py`

The application entry point. Creates the FastAPI app, imports every model so `Base.metadata.create_all()` can build all tables on startup, mounts the `/static` directory, and registers all routers (`trips`, `recommendations`, `votes`, `survey`, `sms_webhook`, plus the web/front-end router). Also exposes a `GET /health` endpoint.

## 7. `app/database.py`

Sets up the SQLAlchemy database layer: creates the `engine` from `settings.database_url` (PostgreSQL), configures `SessionLocal` as the session factory, defines the declarative `Base` class that all models inherit from, and provides the `get_db()` dependency that opens a new session per request and closes it afterward.

---

## Notes

- The frontend (`app/templates`, `app/static`, `app/web/routes.py`) is out of scope for this document.
- The AI gateway abstraction (`app/gateway/`) supports multiple providers, but this project currently runs against a fine-tuned **Llama 3.1** model served via **Ollama**.
