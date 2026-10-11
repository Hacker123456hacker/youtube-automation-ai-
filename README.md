# YouTube Automation AI

A work-in-progress YouTube creator tool with a FastAPI backend and React/Vite frontend. The current MVP can generate a narration-ready script from a topic using the OpenAI API.

> **Implementation status:** AI script generation is implemented. Hindi text-to-speech, image selection, MP4 rendering, YouTube OAuth/upload, analytics, user authentication, and daily scheduling are not yet implemented. Do not assume this repository already publishes videos automatically.

## Current stack

- Backend: FastAPI, SQLAlchemy, Pydantic Settings, OpenAI SDK
- Data services: PostgreSQL and Redis
- Frontend: React, TypeScript, Vite, Tailwind CSS
- Development: Docker Compose and GitHub Actions tests

## Local setup with Docker

1. Install Docker Engine/Desktop and Docker Compose.
2. Copy the backend environment template:
   ```bash
   cp backend/.env.example backend/.env
   ```
3. Set `OPENAI_API_KEY` in `backend/.env` to use script generation. Keep API keys on the backend only.
4. Start the services:
   ```bash
   docker compose up --build
   ```
5. Open:
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000
   - API docs: http://localhost:8000/docs
   - Liveness check: http://localhost:8000/health
   - Database readiness: http://localhost:8000/health/ready

The Compose defaults are for local development only. Set strong `POSTGRES_PASSWORD` and `SECRET_KEY` values before deploying anywhere accessible to other people.

## Generate a script

Use the frontend form or call the backend directly:

```bash
curl -X POST http://localhost:8000/api/content/generate-script \
  -H 'Content-Type: application/json' \
  -d '{"topic":"5 useful AI tools","language":"Hindi","duration_minutes":3,"tone":"engaging and natural"}'
```

The endpoint requires `OPENAI_API_KEY` and uses the `gpt-4o-mini` model. Provider errors return a generic message; check backend logs and your provider account if generation fails.

## Backend local setup

Use Python 3.11 in a virtual environment:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

PostgreSQL must be reachable using `DATABASE_URL`. Development mode creates missing tables at startup; production should use Alembic migrations.

## Environment and security

See `backend/.env.example`. Never commit real API keys, OAuth secrets, or production signing keys. In production set `APP_ENV=production`, keep `DEBUG=false`, and configure a strong random `SECRET_KEY`.

## Roadmap

- [ ] User registration/login and authorization
- [x] AI script generation endpoint and basic frontend form
- [ ] Hindi text-to-speech
- [ ] Licensed image sourcing and FFmpeg video rendering
- [ ] YouTube OAuth and resumable uploads
- [ ] Durable task queue, daily 5 AM scheduler, retries, and duplicate prevention
- [ ] Video download/save flow and upload status tracking
- [ ] Analytics dashboard, migrations, integration tests, and production deployment hardening

## License

MIT
