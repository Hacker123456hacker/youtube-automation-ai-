from app.services.video_pipeline import _sentences


def test_sentences_splits_hindi_punctuation():
    assert _sentences("नमस्ते। यह पहला दृश्य है। अगला दृश्य शुरू।") == [
        "नमस्ते।", "यह पहला दृश्य है।", "अगला दृश्य शुरू।"
    ]


def test_sentences_bounds_scene_count():
    script = " ".join(f"दृश्य {number}।" for number in range(12))
    scenes = _sentences(script)
    assert len(scenes) == 8
    assert "दृश्य 11" in scenes[-1]


def test_sentences_handles_single_line_without_punctuation():
    assert _sentences("यह एक साधारण हिंदी वाक्य है") == ["यह एक साधारण हिंदी वाक्य है"]
