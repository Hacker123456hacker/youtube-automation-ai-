from fastapi import APIRouter, HTTPException
from openai import AsyncOpenAI
from pydantic import BaseModel, Field

from app.config import get_settings

router = APIRouter(prefix="/api/content", tags=["content"])


class ScriptGenerateRequest(BaseModel):
    topic: str = Field(..., min_length=3, max_length=300)
    language: str = Field(default="Hindi", min_length=2, max_length=40)
    duration_minutes: int = Field(default=3, ge=1, le=20)
    tone: str = Field(default="engaging and natural", min_length=3, max_length=100)


class ScriptGenerateResponse(BaseModel):
    topic: str
    language: str
    title: str
    script: str
    estimated_duration_minutes: int


@router.post("/generate-script", response_model=ScriptGenerateResponse)
async def generate_script(payload: ScriptGenerateRequest):
    settings = get_settings()
    if not settings.OPENAI_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="OPENAI_API_KEY is not configured. Add it to backend/.env and restart the backend.",
        )

    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    prompt = (
        "Create an original YouTube video script. Return the response in this format only: "
        "TITLE: one compelling title, then a new line containing SCRIPT:, followed by the spoken script. "
        "Do not include unsupported factual claims. Use short, natural sentences suitable for narration. "
        f"Language: {payload.language}. Topic: {payload.topic}. "
        f"Target length: about {payload.duration_minutes} minutes. Tone: {payload.tone}."
    )
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a careful YouTube scriptwriter. Never claim to have browsed the web."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        result = (response.choices[0].message.content or "").strip()
    except Exception as exc:
        # Avoid returning provider details, API keys, or raw request information.
        raise HTTPException(status_code=502, detail="AI script generation failed. Check the API key and provider status.") from exc
    if not result:
        raise HTTPException(status_code=502, detail="The AI provider returned an empty script.")

    title = f"{payload.topic} | YouTube Script"
    script = result
    if "SCRIPT:" in result.upper():
        split_at = result.upper().find("SCRIPT:")
        heading = result[:split_at].strip()
        script = result[split_at + len("SCRIPT:"):].strip()
        if heading.upper().startswith("TITLE:"):
            title = heading[len("TITLE:"):].strip() or title

    return ScriptGenerateResponse(
        topic=payload.topic,
        language=payload.language,
        title=title,
        script=script,
        estimated_duration_minutes=payload.duration_minutes,
    )
