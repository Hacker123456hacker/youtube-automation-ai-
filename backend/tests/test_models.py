from app.database import Base
from app import models  # noqa: F401


def test_all_expected_tables_are_registered():
    assert {"users", "channels", "content", "videos"} <= set(Base.metadata.tables)
