# TripConsensus

**AI-powered collaborative trip planning platform** built with **FastAPI**, **PostgreSQL**, **Twilio**, **Ollama**, and **Ranked-Choice Voting**.

TripConsensus helps a group of friends/family plan a trip together: each participant fills a short preference survey (budget, dates, climate, activities, food, transport, accommodation), an LLM (via Ollama/OpenAI/Anthropic) turns those preferences into destination recommendations, and the group ranks the recommendations using **Ranked-Choice Voting** to reach a consensus.


---

## Architecture 

```
                    ┌──────────────────────┐
                    │   Participants (web)  │
                    └──────────┬───────────┘
                               │ HTTP
                               ▼
                    ┌──────────────────────┐
                    │   FastAPI app (app/) │   <- app.main:app (assumed entrypoint)
                    └──────────┬───────────┘
                               │
        ┌──────────────┬──────┴───────┬───────────────┐
        ▼              ▼              ▼               ▼
   Schemas         Repositories     Services        Gateway/AI
 (app/schemas)   (app/repositories) (app/services)  (app/gateway,
   Pydantic         SQLAlchemy      business logic   app/prompts,
   request/         data access     e.g. Recommend-  app/ai)
   response         layer over      ationService     talks to
   validation       Postgres                         Ollama / OpenAI /
                                                       Anthropic
        │              │                               │
        ▼              ▼                               ▼
   app/models  ───────────────────────────►   PostgreSQL (Docker: postgres:17)
   (SQLAlchemy ORM: Trip, Participant,
    SurveyResponse, Recommendation, Vote,
    ModelUsage)

   Redis (Docker: redis:7-alpine)  — caching / background task support
   Twilio (twilio SDK)             — SMS notifications to participants
```

**Request flow for a recommendation (traced from `test_recommendation_pipeline.py` / `test_parser.py` / `test_recommendation_service.py`):**

1. `TripRepository` / `SurveyRepository` pull the trip, its participants, and their survey responses from Postgres.
2. `app/prompts/renderer.py` (`renderer.render(...)`) fills a prompt template (e.g. `"destination_recommendation"`) with trip + participant + survey data, producing a `system` / `user` / `output_format` prompt set.
3. `app/gateway/gateway.py` (`Gateway.generate(...)`) sends the prompt to the configured LLM provider (Ollama locally, or OpenAI/Anthropic per `requirements.txt`) and returns the raw response.
4. `app/ai/recommendation_parser.py` (`parser.parse(...)`) parses the raw AI response into structured recommendation data.
5. `app/services/recommendation_service.py` (`RecommendationService.generate_recommendations(trip_id)`) orchestrates steps 1–4 and persists results via `RecommendationRepository`.
6. Participants then vote on the resulting recommendations (`Vote` model / `VoteRepository`) using **Ranked-Choice Voting** to settle on a final destination.

---

## Tech Stack

| Layer | Technology |
|---|---|
| API framework | FastAPI (`fastapi`, `starlette`, `uvicorn`) |
| Database | PostgreSQL 17 (`psycopg2-binary`, `SQLAlchemy`, `alembic` for migrations) |
| Cache / queue | Redis 7 (`redis`, `fakeredis` for tests) |
| Validation | Pydantic v2 (`pydantic`, `pydantic-settings`) |
| AI providers | Ollama (local LLMs), OpenAI SDK, Anthropic SDK |
| Messaging | Twilio (SMS notifications to participants) |
| Auth-related | `passlib`, `bcrypt`, `python-jose`, `PyJWT` (present in dependencies) |
| Testing | `pytest`, `pytest-asyncio`, `pytest-cov`, `freezegun`, `respx` |
| Config | `python-dotenv` (`.env` file), `app/config.py` (`settings` object) |

Full pinned list is in [`requirements.txt`](./requirements.txt).

---

## Project Structure

```
TripConsensus/
├── app/                              # Main application package (FastAPI)
│   ├── database.py                   # SQLAlchemy Base, engine, SessionLocal
│   ├── config.py                     # `settings` object (env-driven config, e.g. Twilio/SMS flags)
│   ├── models/                       # SQLAlchemy ORM models
│   │   ├── trip.py                   # Trip
│   │   ├── participant.py            # Participant
│   │   ├── survey_response.py        # SurveyResponse
│   │   ├── recommendation.py         # Recommendation
│   │   ├── vote.py                   # Vote
│   │   └── model_usage.py            # ModelUsage
│   ├── schemas/                      # Pydantic request/response schemas
│   │   ├── trip.py                   # TripCreate
│   │   ├── participant.py            # ParticipantCreate
│   │   ├── survey_response.py        # SurveyResponseCreate
│   │   ├── recommendation.py         # RecommendationCreate
│   │   └── vote.py                   # VoteCreate
│   ├── repositories/                 # Data-access layer (one repo per model)
│   │   ├── trip_repository.py        # TripRepository
│   │   ├── participant_repository.py # ParticipantRepository
│   │   ├── survey_repository.py      # SurveyRepository
│   │   ├── recommendation_repository.py # RecommendationRepository
│   │   ├── vote_repository.py        # VoteRepository
│   │   └── model_usage_repository.py # ModelUsageRepository
│   ├── services/
│   │   └── recommendation_service.py # RecommendationService   core business logic
│   ├── gateway/
│   │   └── gateway.py                # Gateway   unified AI-provider client
│   ├── prompts/
│   │   └── renderer.py               # renderer   prompt-template rendering
│   ├── ai/
│   │   └── recommendation_parser.py  # parser     parses raw AI output
│   ├── routers/                      #  FastAPI route modules
│   └── main.py                       # FastAPI app entrypoint
├── scripts/                          # 
├── create_tables.py                  # Creates all DB tables from the models
├── docker-compose.yml                # Postgres 17 + Redis 7 services
├── requirements.txt                  # Python dependencies
├── test_config.py                    # 
├── test_database.py                  # 
├── test_db_types.py                  # 
├── test_gateway.py                   # Manual  test for Gateway.generate()
├── test_models.py                    # Sanity import-check for all ORM models
├── test_parser.py                    # End-to-end: render → generate → parse
├── test_recommendation_pipeline.py   # End-to-end: render → generate (raw output)
├── test_recommendation_service.py    # End-to-end: RecommendationService.generate_recommendations()
├── test_repositories.py              # Exercises create/read methods on every repository
├── test_schemas.py                   # Sanity import-check for all Pydantic schemas
└── test_twilio_config.py             # Prints Twilio-related settings
```


---

## File-by-File Reference

### Root scripts

#### `create_tables.py`
Imports the SQLAlchemy `Base` / `engine` from `app.database` and every model (`Trip`, `Participant`, `SurveyResponse`, `Recommendation`, `Vote`, `ModelUsage`), then runs `Base.metadata.create_all(bind=engine)` to create all tables in Postgres. Run this once after starting the database.

### `app/database.py` *(inferred from imports)*
- `Base` — SQLAlchemy declarative base, used by all ORM models.
- `engine` — SQLAlchemy engine (Postgres connection).
- `SessionLocal` — session factory used throughout repositories/services (`db = SessionLocal()`).

### `app/config.py` *(inferred from imports)*
- `settings` — a Pydantic-settings object loaded from environment variables (`.env`). Confirmed attributes: `enable_sms`, `twilio_account_sid`, `twilio_phone_number`. Almost certainly also holds DB URL, Redis URL, and AI-provider credentials.

### `app/models/` — SQLAlchemy ORM models
| File | Class | Notes |
|---|---|---|
| `trip.py` | `Trip` | Has `title`, `description`; related to `Participant`s, `Recommendation`s |
| `participant.py` | `Participant` | Has `trip_id`, `name`, `phone_number`, `email`, `is_organizer` |
| `survey_response.py` | `SurveyResponse` | Has `participant_id`, `budget_per_person`, `available_from`/`available_to`, `preferred_climates`, `preferred_activities`, `food_preferences`, `transport_preferences`, `accommodation_preferences`, `additional_notes` |
| `recommendation.py` | `Recommendation` | Has `trip_id`, `destination`, `recommended_start_date`/`end_date`, `reason`, `estimated_cost`, `confidence_score`, `model_provider`, `model_name`, `prompt_version` |
| `vote.py` | `Vote` | Has `participant_id`, `recommendation_id`, `rank` — the raw data behind Ranked-Choice Voting |
| `model_usage.py` | `ModelUsage` | Has `trip_id`, `provider`, `model_name`, `prompt_version`, `input_tokens`, `output_tokens`, `response_time`, `estimated_cost` — tracks AI usage/cost |

### `app/schemas/` — Pydantic schemas (API layer)
`trip.py` (`TripCreate`), `participant.py` (`ParticipantCreate`), `survey_response.py` (`SurveyResponseCreate`), `recommendation.py` (`RecommendationCreate`), `vote.py` (`VoteCreate`) — request-validation models mirroring the ORM models above.

### `app/repositories/` — data-access layer
Each repository wraps a `db: Session` and exposes CRUD-style methods.

| File | Class | Confirmed methods |
|---|---|---|
| `trip_repository.py` | `TripRepository` | `create()`, `exists(id)`, `get_by_id(id)`, `search_by_title(text)` |
| `participant_repository.py` | `ParticipantRepository` | `create()`, `exists(id)`, `get_by_phone_number(phone)` |
| `survey_repository.py` | `SurveyRepository` | `create()`, `exists(id)`, `get_by_participant_id(id)`, `get_by_trip_id(trip_id)` |
| `recommendation_repository.py` | `RecommendationRepository` | `create()`, `exists(id)`, `get_best_recommendation(trip_id)` |
| `vote_repository.py` | `VoteRepository` | `create()`, `exists(id)` |
| `model_usage_repository.py` | `ModelUsageRepository` | `create()`, `exists(id)`, `get_total_estimated_cost()` |

### `app/gateway/gateway.py` 
- **`Gateway`** — unified client to the AI backends. Exposes `generate(system_prompt, user_prompt) -> response` (returns an object with a `.content` attribute). Backed by `ollama`, `openai`, and `anthropic` SDKs per `requirements.txt`, so it likely selects a provider based on `app.config.settings`.

### `app/prompts/renderer.py` 
- **`renderer`** — renders named prompt templates. Confirmed usage: `renderer.render("destination_recommendation", trip=..., participants=..., survey_responses=...)`, returning a dict with `system`, `user`, and optionally `output_format` keys.

### `app/ai/recommendation_parser.py` 
- **`parser`** — parses the raw LLM response object into structured recommendation data. Confirmed usage: `parser.parse(response)`.

### `app/services/recommendation_service.py` 
- **`RecommendationService`** — orchestrates the full pipeline. Constructed with `db`, `recommendation_repository`, `survey_repository`, `trip_repository`, `gateway`. Exposes `generate_recommendations(trip_id)`, which renders the prompt, calls the `Gateway`, parses the result, and (presumably) persists it via `RecommendationRepository`.

### `app/main.py`, `app/routers/`, `scripts/` 
Not directly reachable through automated browsing of this repo — GitHub returns a robots-disallowed response for folder/tree URLs. Based on the stack (FastAPI + the modules above), `app/main.py` is almost certainly the FastAPI app entrypoint (`app = FastAPI()`), wired to route modules under `app/routers/` for trips, participants, surveys, recommendations, and votes, plus a Twilio webhook/notification route. **Please add the real contents/paths here once verified.**

### Test / smoke scripts (root level)
These are **manual smoke-test scripts** (run directly with `python test_x.py`), not `pytest`-style test suites, despite `pytest` being a dependency:

| File | What it does |
|---|---|
| `test_models.py` | Imports every ORM model to confirm they load without error |
| `test_schemas.py` | Imports every Pydantic schema to confirm they load without error |
| `test_repositories.py` | Creates a `Trip` → `Participant` → `SurveyResponse` → `Recommendation` → `Vote` → `ModelUsage` end-to-end and asserts each repository's methods work |
| `test_gateway.py` | Calls `Gateway.generate()` directly with a hard-coded travel-recommendation prompt |
| `test_recommendation_pipeline.py` | Loads a trip by hard-coded ID, renders the prompt, calls the gateway, prints the raw AI response |
| `test_parser.py` | Same as above, plus runs the raw AI response through `recommendation_parser.parser.parse()` |
| `test_recommendation_service.py` | Instantiates `RecommendationService` and calls `generate_recommendations(trip_id)` end-to-end |
| `test_twilio_config.py` | Prints `settings.enable_sms`, `settings.twilio_account_sid`, `settings.twilio_phone_number` to verify Twilio config is loaded |
| `test_config.py`, `test_database.py`, `test_db_types.py` |`app.config.settings` loading, DB connectivity, and custom SQLAlchemy column types respectively |

### `docker-compose.yml`
Spins up local infrastructure:
- `postgres` — Postgres 17, container `tripplanner_postgres`, DB `tripplanner`, exposed on `5432`, with a persistent `postgres_data` volume.
- `redis` — Redis 7 (alpine), container `tripplanner_redis`, exposed on `6379`.

---

## Getting Started

> The exact run command for the API (e.g. `uvicorn app.main:app --reload`) is **assumed** since `app/main.py` wasn't directly inspected — confirm/update once verified.

1. **Clone the repo**
   ```bash
   git clone https://github.com/tanvi-vasoya/TripConsensus.git
   cd TripConsensus
   ```

2. **Start infrastructure (Postgres + Redis)**
   ```bash
   docker-compose up -d
   ```

3. **Create a virtual environment and install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file (loaded via `python-dotenv` / `app/config.py`). At minimum you'll need a Postgres connection URL matching `docker-compose.yml` (`postgresql://postgres:password@localhost:5432/tripplanner`), plus Twilio and AI-provider credentials, e.g.:
   ```env
   DATABASE_URL=postgresql://postgres:password@localhost:5432/tripplanner
   REDIS_URL=redis://localhost:6379

   ENABLE_SMS=false
   TWILIO_ACCOUNT_SID=
   TWILIO_AUTH_TOKEN=
   TWILIO_PHONE_NUMBER=

   # AI provider (Ollama / OpenAI / Anthropic — check app/config.py for exact var names)
   OLLAMA_MODEL=llama3.2
   OPENAI_API_KEY=
   ANTHROPIC_API_KEY=
   ```

5. **Create database tables**
   ```bash
   python create_tables.py
   ```

6. **Run the API** *(assumed entrypoint — confirm against `app/main.py`)*
   ```bash
   uvicorn app.main:app --reload
   ```

7. **Try the smoke-test scripts** (after seeding some data, e.g. via `test_repositories.py`)
   ```bash
   python test_repositories.py
   python test_recommendation_pipeline.py
   python test_recommendation_service.py
   ```

---

