from app.config import Settings


def test_cors_origins_accept_json_array():
    settings = Settings(CORS_ORIGINS='["http://localhost:3000","http://localhost:5173"]')
    assert settings.cors_origins == ["http://localhost:3000", "http://localhost:5173"]


def test_cors_origins_accept_comma_separated_values():
    settings = Settings(CORS_ORIGINS="http://localhost:3000, http://localhost:5173")
    assert settings.cors_origins == ["http://localhost:3000", "http://localhost:5173"]
