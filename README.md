# YouTube Automation AI

A work-in-progress YouTube creator tool with a FastAPI backend and React/Vite frontend. The current MVP can generate a narration-ready script from a topic using the OpenAI API.

> **Implementation status:** AI script generation and a first Hindi narration + Wikimedia Commons visuals + vertical MP4 rendering endpoint are implemented on this branch. YouTube OAuth/upload, analytics, user authentication, and daily scheduling are still not implemented. This branch does not publish videos automatically.

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

## Render a narrated Hindi MP4

The `POST /api/video/render` endpoint accepts a topic, title, and script, then returns a vertical 720×1280 MP4 as a direct download. It uses the online Hindi voice `hi-IN-SwaraNeural`, FFmpeg, and searches Wikimedia Commons for visuals. A generated background card is used when a suitable Commons image cannot be found. The temporary render also records source/licence metadata in `visual_credits.json`; verify each image licence before publishing.

Example (save the response as `hindi-video.mp4`):

```bash
curl -X POST http://localhost:8000/api/video/render \
  -H 'Content-Type: application/json' \
  --output hindi-video.mp4 \
  -d '{"topic":"जल संरक्षण","title":"पानी बचाना क्यों जरूरी है","script":"पानी हमारे जीवन के लिए बहुत जरूरी है। हमें पानी को बर्बाद नहीं करना चाहिए। घर में नल बंद रखें और बारिश के पानी को जमा करें। छोटे कदम भी बड़ा बदलाव ला सकते हैं।"}'
```

This needs internet access for the voice and Commons search, plus FFmpeg/ffprobe. The Docker image installs FFmpeg and a Devanagari font. To save the MP4 on Android, download the response in the phone browser or run the command in Termux. The endpoint is not an offline voice model.

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
- [x] Hindi text-to-speech and first MP4 rendering endpoint (live integration test still needed)
- [x] Wikimedia Commons visual search with source/licence metadata
- [ ] YouTube OAuth and resumable uploads
- [ ] Durable task queue, daily 5 AM scheduler, retries, and duplicate prevention
- [ ] Video download/save flow and upload status tracking
- [ ] Analytics dashboard, migrations, integration tests, and production deployment hardening

## License

MIT
