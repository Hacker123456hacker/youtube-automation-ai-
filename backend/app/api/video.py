import shutil
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from starlette.background import BackgroundTask

from app.services.video_pipeline import VideoPipelineError, render_hindi_video

router = APIRouter(prefix="/api/video", tags=["video"])


class RenderVideoRequest(BaseModel):
    topic: str = Field(..., min_length=3, max_length=300)
    title: str = Field(..., min_length=3, max_length=180)
    script: str = Field(..., min_length=20, max_length=12000)


@router.post("/render")
async def render_video(payload: RenderVideoRequest):
    """Generate and return a vertical MP4; the response is a direct download."""
    try:
        output, work_dir = await render_hindi_video(
            topic=payload.topic,
            title=payload.title,
            script=payload.script,
        )
    except VideoPipelineError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        # Do not expose stack traces or third-party response details to API callers.
        raise HTTPException(status_code=502, detail="Video generation failed. Check backend logs and installed media dependencies.") from exc

    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in payload.title).strip("_")[:60] or "hindi-video"
    return FileResponse(
        path=output,
        media_type="video/mp4",
        filename=f"{safe_name}.mp4",
        background=BackgroundTask(shutil.rmtree, str(work_dir), ignore_errors=True),
    )
