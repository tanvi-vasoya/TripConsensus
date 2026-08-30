# TripConsensus

AI-powered collaborative trip planning platform that helps groups agree on a destination — fast. Participants fill out a short survey, an LLM turns everyone's preferences into ranked destination recommendations, and the group settles it with Ranked Choice Voting.

## Features

- **Group trip creation** — spin up a trip and invite participants to weigh in.
- **Preference surveys** — collect each participant's budget, dates, and travel preferences.
- **AI-generated recommendations** — a pluggable LLM gateway (supports OpenAI, Anthropic, and local models via Ollama) turns survey responses into structured destination suggestions with estimated cost, dates, and a confidence score.
- **Ranked Choice Voting** — participants rank the recommended destinations and the platform tallies an instant-runoff winner, so the group lands on a pick everyone can live with.
- **SMS notifications** — Twilio integration for sending survey links and updates to participants.
- **Usage tracking** — model calls are logged (`ModelUsage`) for cost and performance visibility.

## Tech Stack

| Layer          | Technology                          |
|----------------|--------------------------------------|
| API            | FastAPI, Uvicorn                     |
| Database       | PostgreSQL, SQLAlchemy, Alembic      |
| Caching        | Redis                                |
| AI / LLM       | OpenAI, Anthropic, Ollama (pluggable gateway) |
| Messaging      | Twilio                               |
| Auth           | JWT (python-jose), Passlib, bcrypt   |
| Testing        | Pytest, pytest-asyncio, coverage     |

## Project Structure

```
TripConsensus/
├── app/                    # Application source (API, models, services, gateway)
├── scripts/                # Utility / one-off scripts
├── create_tables.py        # Creates all database tables from SQLAlchemy models
├── docker-compose.yml      # Local PostgreSQL + Redis services
├── requirements.txt        # Python dependencies
└── test_*.py                # Test suite (config, database, models, gateway, voting, etc.)
```

Core data models include `Trip`, `Participant`, `SurveyResponse`, `Recommendation`, `Vote`, and `ModelUsage`.

## Getting Started

### Prerequisites

- Python 3.11+
- Docker (for PostgreSQL and Redis)
- A Twilio account (for SMS features)
- An OpenAI / Anthropic API key, and/or a local [Ollama](https://ollama.com) install

### 1. Clone the repository

```bash
git clone https://github.com/tanvi-vasoya/TripConsensus.git
cd TripConsensus
```

### 2. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Start PostgreSQL and Redis

```bash
docker-compose up -d
```

This starts:
- PostgreSQL on `localhost:5432` (db: `tripplanner`, user: `postgres`, password: `password`)
- Redis on `localhost:6379`

### 4. Configure environment variables

Create a `.env` file in the project root with your database, Twilio, and AI provider credentials (e.g. `DATABASE_URL`, `REDIS_URL`, `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.) — see `app/config.py` for the full list of expected settings.

### 5. Create database tables

```bash
python create_tables.py
```

### 6. Run the API

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs`.

## Running Tests

```bash
pytest
```

With coverage:

```bash
pytest --cov=app
```

## How It Works

1. A user creates a **Trip** and invites **Participants**.
2. Each participant submits a **Survey Response** with their budget, availability, and preferences (optionally collected via Twilio SMS).
3. The **Gateway** service sends the aggregated preferences to an LLM (OpenAI, Anthropic, or a local Ollama model) and receives structured **Recommendations** — destinations with dates, estimated cost, and a confidence score.
4. Participants **Vote** by ranking the recommendations.
5. The platform runs **Ranked Choice Voting** (instant-runoff) on the votes to determine the group's consensus destination.

## Contributing

Contributions are welcome — feel free to open an issue or submit a pull request.

## License

No license has been specified for this repository yet.
