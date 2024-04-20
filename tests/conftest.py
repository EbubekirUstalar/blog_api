import pytest


@pytest.fixture(autouse=True)
def enable_db_access(db):
    # always connect to db
    pass
