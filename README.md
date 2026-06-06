# YouTube Automation AI 🎬

Complete AI-powered YouTube content automation platform. Generate, edit, and publish videos automatically using GPT-4, ElevenLabs, and YouTube API.

## Features ✨

✅ AI Content Generation - GPT-4 powered script writing
✅ Voice Generation - ElevenLabs text-to-speech
✅ Video Creation - Automated video generation
✅ Thumbnail Generation - AI-powered thumbnails
✅ YouTube Integration - Direct upload to YouTube
✅ Analytics Dashboard - Real-time metrics
✅ Content Scheduling - Schedule uploads
✅ Multi-channel Support - Manage multiple channels
✅ Task Queue - Celery for background jobs
✅ Docker Ready - Complete containerization

## Tech Stack 🛠️

### Backend
- FastAPI - Modern async web framework
- PostgreSQL - Database
- SQLAlchemy - ORM
- Celery - Task queue
- Redis - Cache & message broker
- OpenAI - GPT-4 API
- ElevenLabs - Voice generation

### Frontend
- React 18 - UI framework
- TypeScript - Type safety
- Tailwind CSS - Styling
- Zustand - State management
- Axios - HTTP client

### DevOps
- Docker - Containerization
- Docker Compose - Orchestration
- PostgreSQL - Database
- Redis - Cache

## Quick Start 🚀

### Using Docker

```bash
# Clone repository
git clone https://github.com/Hacker123456hacker/youtube-automation-ai-.git
cd youtube-automation-ai-

# Copy environment
cp backend/.env.example backend/.env

# Update .env with your API keys

# Start all services
docker-compose up -d

# Access
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Local Development

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## API Documentation

Visit http://localhost:8000/docs for interactive API documentation.

## Key Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `POST /api/auth/refresh` - Refresh token

### Content
- `GET /api/content` - List content
- `POST /api/content/generate` - Generate content with AI
- `GET /api/content/{id}` - Get content detail

### YouTube
- `POST /api/youtube/connect` - Connect YouTube account
- `GET /api/youtube/channels` - List channels
- `POST /api/youtube/upload` - Upload video

### Analytics
- `GET /api/analytics/dashboard` - Dashboard metrics

## Project Structure

```
youtube-automation-ai-/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── main.py
│   │   └── config.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## License

MIT License

---

**Made with ❤️ for YouTube Creators**
