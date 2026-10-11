# YouTube Automation AI

Starter project for a YouTube automation platform. The repository currently contains a basic FastAPI backend, SQLAlchemy models, a minimal React/Vite frontend, and Docker Compose infrastructure.

> **Implementation status:** This is not yet a complete video automation product. Authentication, AI script generation, text-to-speech, video rendering, YouTube OAuth/upload, analytics, and scheduled jobs still need to be implemented and tested. The API routes listed in older versions of this README should not be assumed to exist.

## Current stack

- Backend: FastAPI, SQLAlchemy, Pydantic Settings
- Data services: PostgreSQL and Redis (Redis/Celery workers are not yet wired to a generation workflow)
- Frontend: React, TypeScript, Vite, Tailwind CSS
- Container development: Docker Compose

## Local setup with Docker

1. Install Docker Engine/Desktop and Docker Compose.
2. Copy the environment template and replace all example secrets:
   ```bash
   cp backend/.env.example backend/.env
   ```
3. Start the development services:
   ```bash
   docker compose up --build
   ```
4. Open:
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000
   - API docs: http://localhost:8000/docs
   - Liveness check: http://localhost:8000/health
   - Database readiness: http://localhost:8000/health/ready

The compose file uses a development-only database password by default. Override `POSTGRES_PASSWORD` and `SECRET_KEY` before using this outside a local development environment.

## Backend local setup

Use Python 3.11 in a virtual environment:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The backend expects PostgreSQL to be reachable using `DATABASE_URL`. For production, use Alembic migrations instead of relying on automatic table creation.

## Environment variables

See `backend/.env.example`. Never commit real API keys, OAuth client secrets, or production signing keys. In production set `APP_ENV=production`, set `DEBUG=false`, and configure a strong random `SECRET_KEY`.

## Roadmap

- [ ] Add and test registration/login and authorization
- [ ] Implement AI topic and script generation
- [ ] Implement Hindi text-to-speech
- [ ] Implement licensed-image selection and FFmpeg rendering
- [ ] Implement YouTube OAuth and resumable upload
- [ ] Add a durable task queue, daily scheduler, retries, and duplicate prevention
- [ ] Build a functional dashboard and video download flow
- [ ] Add migrations, tests, CI, logging, and production deployment documentation

## License

MIT
