import os
import sys
from datetime import timedelta
from pathlib import Path

import pytest
import responses
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from fastapi_login import LoginManager
from sqlalchemy.exc import OperationalError

from routine_tracker_core.settings import get_db_settings, get_settings
from routine_tracker_core.tests.factories import RoutineFactory, UserFactory


def _set_pythonpath():
    """
    Set PYTHONPATH so pytest wont complain about missing __init__.py
    """
    sys.path.append(str(Path(__file__).parent))


class RequestsMock(responses.RequestsMock):
    @property
    def call_count(self):
        return len(self.calls)


@pytest.fixture
def requests_mock():
    with RequestsMock() as _requests_mock:
        yield _requests_mock


@pytest.fixture(scope="session")
def client():
    from routine_tracker_core.external_interfaces.routine_tracker_api.main import app

    return TestClient(app)


def drop_all(engine):
    from routine_tracker_core.database import RoutineTrackerCoreBaseModel as Base

    with engine.begin() as conn:
        conn.exec_driver_sql("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
    Base.metadata.drop_all(bind=engine)


def _run_alembic_upgrade():
    config = Config("alembic.ini")
    command.upgrade(config, "head")


@pytest.fixture(scope="session")
def db_engine():
    from routine_tracker_core.database import get_engine

    engine = get_engine()
    try:
        engine.connect()
    except OperationalError as err:
        if "Connection refused" in str(err):
            suggestion = "Is your db up and running?\nsuggestion: docker-compose up -d"
        elif "does not exist" in str(err):
            suggestion = (
                "Did you create a local test database?\n"
                "suggestion: docker-compose exec db createdb -U test -O test testdb"
            )
        else:
            raise err

        raise AssertionError(suggestion) from err

    drop_all(engine)

    _run_alembic_upgrade()
    yield engine

    drop_all(engine)
    engine.dispose()


@pytest.fixture
def db_session(db_engine):
    from routine_tracker_core.database import SessionLocal

    with SessionLocal(bind=db_engine) as db:
        _run_alembic_upgrade()
        yield db
        db.rollback()
        drop_all(db_engine)


@pytest.fixture(autouse=True)
def self_destructible_db(db_engine):
    """
    Ensure db is in a clean state before and after the test.
    """
    drop_all(engine=db_engine)
    _run_alembic_upgrade()

    yield

    drop_all(engine=db_engine)
    _run_alembic_upgrade()


@pytest.fixture(autouse=True, scope="session")
def _envvars(tmpdir_factory, session_mocker):
    os.environ.setdefault("TEST_DATABASE_URL", "postgresql://test:test@localhost:54321/testdb")
    mock_envvars = dict(
        DATABASE_URL=os.environ["TEST_DATABASE_URL"],
    )
    session_mocker.patch.dict(os.environ, mock_envvars)
    settings = get_settings()
    get_db_settings()
    _safety_checks(settings)
    _set_pythonpath()


def _safety_checks(settings):
    assert (
        "test" in settings.DATABASE_URL.path
    ), f"TEST_DATABASE_URL database MUST have 'test' in its name (got {settings.DATABASE_URL.path=})"


@pytest.fixture
def valid_current_token():
    return LoginManager().create_access_token(
        data=dict(email="user_1@email.com", google_token="TOKEN"),
        expires=timedelta(hours=get_settings().TOKEN_EXPIRATION_HOURS),
    )


@pytest.fixture(autouse=True)
def reset_factory_boy_sequences():
    UserFactory.reset_sequence(0)
    RoutineFactory.reset_sequence(0)
