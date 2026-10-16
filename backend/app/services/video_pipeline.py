"""Render a vertical narrated MP4 from a Hindi script and Wikimedia Commons visuals."""
from __future__ import annotations

import asyncio
import json
import re
import shutil
import subprocess
import tempfile
import textwrap
from pathlib import Path
from typing import Any

import edge_tts
import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps

COMMONS_API = "https://commons.wikimedia.org/w/api.php"
VOICE = "hi-IN-SwaraNeural"
WIDTH, HEIGHT = 720, 1280
MAX_SCENES = 8
MAX_IMAGE_BYTES = 12 * 1024 * 1024
FONT_CANDIDATES = (
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
)


class VideoPipelineError(RuntimeError):
    """Raised when a requested video cannot be produced safely."""


def _run(command: list[str]) -> None:
    try:
        result = subprocess.run(command, check=False, capture_output=True, text=True, timeout=180)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise VideoPipelineError("FFmpeg is unavailable or timed out. Install FFmpeg and retry.") from exc
    if result.returncode:
        raise VideoPipelineError("FFmpeg failed while rendering the video.")


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in FONT_CANDIDATES:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


def _sentences(script: str) -> list[str]:
    parts = [p.strip() for p in re.split(r"(?<=[।.!?])\s+|\n+", script) if p.strip()]
    if not parts:
        parts = [script.strip()]
    # Keep the number of scenes bounded for memory and render time.
    groups: list[str] = []
    for part in parts:
        if len(groups) < MAX_SCENES:
            groups.append(part)
        else:
            groups[-1] += " " + part
    return groups


def _commons_image(query: str, destination: Path) -> dict[str, str] | None:
    headers = {"User-Agent": "YouTubeAutomationAI/0.1 (educational video renderer)"}
    try:
        response = requests.get(
            COMMONS_API,
            params={
                "action": "query", "format": "json", "generator": "search",
                "gsrsearch": f'filetype:bitmap {query}', "gsrnamespace": 6,
                "gsrlimit": 8, "prop": "imageinfo", "iiprop": "url|extmetadata",
                "iiurlwidth": 1000,
            },
            headers=headers, timeout=15,
        )
        response.raise_for_status()
        pages = response.json().get("query", {}).get("pages", {})
        for page in pages.values():
            info = (page.get("imageinfo") or [{}])[0]
            url = info.get("thumburl") or info.get("url")
            if not url or not url.startswith("https://upload.wikimedia.org/"):
                continue
            image_response = requests.get(url, headers=headers, timeout=20, stream=True)
            image_response.raise_for_status()
            content_type = image_response.headers.get("Content-Type", "")
            if not content_type.startswith("image/"):
                continue
            size = 0
            with destination.open("wb") as output:
                for chunk in image_response.iter_content(65536):
                    size += len(chunk)
                    if size > MAX_IMAGE_BYTES:
                        output.close()
                        destination.unlink(missing_ok=True)
                        break
                    output.write(chunk)
            if not destination.exists() or destination.stat().st_size == 0 or size > MAX_IMAGE_BYTES:
                continue
            try:
                with Image.open(destination) as img:
                    img.verify()
            except Exception:
                destination.unlink(missing_ok=True)
                continue
            metadata = info.get("extmetadata", {})
            artist = re.sub("<[^>]+>", "", metadata.get("Artist", {}).get("value", "Unknown creator"))
            license_name = metadata.get("LicenseShortName", {}).get("value", "Check source page")
            return {
                "title": page.get("title", "Wikimedia Commons image"),
                "source_url": info.get("descriptionurl", ""),
                "image_url": url,
                "artist": artist[:300],
                "license": license_name[:100],
            }
    except (requests.RequestException, ValueError, OSError):
        return None
    return None


def _make_card(source: Path, destination: Path, title: str, caption: str) -> None:
    try:
        with Image.open(source) as opened:
            image = ImageOps.fit(opened.convert("RGB"), (WIDTH, HEIGHT), method=Image.Resampling.LANCZOS)
    except Exception as exc:
        raise VideoPipelineError("A downloaded visual could not be decoded.") from exc
    # Dark gradient panels make captions readable on mobile.
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for y in range(HEIGHT):
        alpha = int(175 * max(0, (y - HEIGHT * 0.55) / (HEIGHT * 0.45)))
        if alpha:
            draw.line((0, y, WIDTH, y), fill=(0, 0, 0, alpha))
    draw.rectangle((0, 0, WIDTH, 190), fill=(0, 0, 0, 110))
    image = Image.alpha_composite(image.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(image)
    title_font, caption_font = _font(36), _font(31)
    draw.multiline_text((38, 35), "\n".join(textwrap.wrap(title, 28)[:2]), font=title_font, fill="white", stroke_width=1, stroke_fill="black", spacing=8)
    caption_lines = textwrap.wrap(caption, 34)
    visible = "\n".join(caption_lines[-5:])
    draw.multiline_text((38, HEIGHT - 300), visible, font=caption_font, fill="white", stroke_width=1, stroke_fill="black", spacing=10)
    image.convert("RGB").save(destination, quality=92)


async def render_hindi_video(topic: str, title: str, script: str) -> tuple[Path, Path]:
    """Return (mp4_path, temp_directory); caller must clean the directory after response."""
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise VideoPipelineError("FFmpeg and ffprobe are required. Install FFmpeg first.")
    clean_script = script.strip()
    if len(clean_script) < 20:
        raise VideoPipelineError("Script is too short; provide at least 20 characters.")
    if len(clean_script) > 12000:
        raise VideoPipelineError("Script is too long; limit it to 12,000 characters.")
    work = Path(tempfile.mkdtemp(prefix="yt-auto-video-"))
    try:
        audio_path = work / "narration.mp3"
        communicate = edge_tts.Communicate(clean_script, VOICE)
        await communicate.save(str(audio_path))
        if not audio_path.exists() or audio_path.stat().st_size < 1000:
            raise VideoPipelineError("Hindi voice generation returned an empty audio file.")
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)],
            check=True, capture_output=True, text=True, timeout=30,
        )
        audio_duration = max(1.0, float(probe.stdout.strip()))
        scenes = _sentences(clean_script)
        weights = [max(1, len(scene.split())) for scene in scenes]
        total_weight = sum(weights)
        clips: list[Path] = []
        credits: list[dict[str, str]] = []
        for index, scene in enumerate(scenes):
            image_path = work / f"source-{index:02d}.jpg"
            visual_query = scene[:120] if index else topic[:120]
            credit = await asyncio.to_thread(_commons_image, visual_query, image_path)
            if credit is None:
                # A generated gradient card is a safe offline fallback; no unlicensed random image.
                base = Image.new("RGB", (WIDTH, HEIGHT), (24, 39, 70))
                d = ImageDraw.Draw(base)
                d.ellipse((80, 180, 640, 740), fill=(43, 94, 130))
                d.text((60, 850), "VISUAL", font=_font(48), fill="white")
                base.save(image_path, quality=90)
                credit = {"title": "Generated fallback background", "source_url": "", "image_url": "", "artist": "Generated locally", "license": "Original generated background"}
            credits.append({"scene": str(index + 1), **credit})
            card = work / f"scene-{index:02d}.jpg"
            _make_card(image_path, card, title, scene)
            duration = max(1.0, audio_duration * weights[index] / total_weight)
            clip = work / f"clip-{index:02d}.mp4"
            _run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", "25", "-i", str(card), "-t", f"{duration:.3f}", "-vf", "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,format=yuv420p", "-r", "25", "-an", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "27", str(clip)])
            clips.append(clip)
        concat_file = work / "clips.txt"
        concat_file.write_text("".join(f"file '{clip.as_posix()}'\n" for clip in clips), encoding="utf-8")
        silent_video = work / "silent.mp4"
        _run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(concat_file), "-c", "copy", str(silent_video)])
        output = work / "video.mp4"
        _run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(silent_video), "-i", str(audio_path), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", str(output)])
        (work / "visual_credits.json").write_text(json.dumps(credits, ensure_ascii=False, indent=2), encoding="utf-8")
        return output, work
    except Exception:
        shutil.rmtree(work, ignore_errors=True)
        raise
