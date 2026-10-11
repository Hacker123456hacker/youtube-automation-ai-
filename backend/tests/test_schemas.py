import pytest
from pydantic import ValidationError

from app.schemas import ContentCreate, LoginRequest, UserCreate


def test_user_create_accepts_valid_email_and_password():
    payload = UserCreate(email="creator@example.com", username="creator_01", password="long-password")
    assert payload.email == "creator@example.com"


@pytest.mark.parametrize("email", ["not-an-email", "missing-domain@", "@missing-user.com"])
def test_user_create_rejects_invalid_email(email):
    with pytest.raises(ValidationError):
        UserCreate(email=email, username="creator_01", password="long-password")


def test_login_rejects_invalid_email():
    with pytest.raises(ValidationError):
        LoginRequest(email="bad-email", password="anything")


def test_content_create_requires_title_and_topic():
    with pytest.raises(ValidationError):
        ContentCreate(title="", topic="test")
