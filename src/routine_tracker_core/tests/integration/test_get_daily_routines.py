from datetime import date, datetime, timedelta

import pytest
from fastapi_login import LoginManager
from freezegun import freeze_time

from routine_tracker_core.domain.constants import PeriodicyEnum
from routine_tracker_core.settings import get_settings
from routine_tracker_core.tests.factories import FrequencyFactory, RoutineFactory, TrackerFactory, UserFactory

route_uri = "/routine/daily"

settings = get_settings()


def current_date():
    return datetime(2024, 7, 27)


@pytest.fixture
@freeze_time(current_date)
def current_test_token():
    return LoginManager(settings.JWT_SECRET.get_secret_value(), "/auth").create_access_token(
        data=dict(email="user_1@email.com", google_token="TOKEN"),
        expires=timedelta(hours=settings.TOKEN_EXPIRATION_HOURS),
    )


@pytest.fixture
@freeze_time(current_date)
def database_populated(db_session):
    user = UserFactory()
    routines = [
        RoutineFactory(user=user, quantity=2),
        RoutineFactory(user=user, quantity=2, periodicy=PeriodicyEnum.WEEKLY),
        RoutineFactory(user=user, quantity=2),
    ]
    frequencies = [
        FrequencyFactory(routine=routines[0], day=0),
        FrequencyFactory(routine=routines[0], day=2),
        FrequencyFactory(routine=routines[2], day=4),
    ]
    trackers = [
        TrackerFactory(routine=routines[0], date=date(2024, 7, 22), done=1),
        TrackerFactory(routine=routines[1], date=date(2024, 7, 15), done=2),
        TrackerFactory(routine=routines[1], date=date(2024, 7, 22), done=2),
    ]

    db_session.add(user)
    db_session.add_all(routines)
    db_session.add_all(frequencies)
    db_session.add_all(trackers)
    db_session.commit()


@pytest.fixture
@freeze_time(current_date)
def database_populated_only_daily(db_session):
    user = UserFactory()
    routines = [
        RoutineFactory(user=user, quantity=2),
        RoutineFactory(user=user, quantity=2),
    ]
    frequencies = [
        FrequencyFactory(routine=routines[0], day=0),
        FrequencyFactory(routine=routines[0], day=2),
        FrequencyFactory(routine=routines[1], day=4),
    ]
    trackers = [
        TrackerFactory(routine=routines[0], date=date(2024, 7, 22), done=1),
    ]

    db_session.add(user)
    db_session.add_all(routines)
    db_session.add_all(frequencies)
    db_session.add_all(trackers)
    db_session.commit()


@freeze_time(current_date)
def test_endpoint_success(self_destructible_db, database_populated, client, current_test_token):
    formated_date = (datetime.today() - timedelta(days=5)).strftime("%Y-%m-%d")
    response = client.get(
        f"{route_uri}?date={formated_date}",
        headers={"Authorization": f"Bearer {current_test_token}"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Routines found successfully",
        "routines": [
            {
                "id": 1,
                "title": "ROUTINE 1",
                "qty_done": 1,
                "qty_total": 2,
            },
            {
                "id": 2,
                "title": "ROUTINE 2",
                "qty_done": 2,
                "qty_total": 2,
            },
        ],
    }


@freeze_time(current_date)
def test_endpoint_return_empty(self_destructible_db, database_populated_only_daily, client, current_test_token):
    formated_date = datetime.today().strftime("%Y-%m-%d")
    response = client.get(
        f"{route_uri}?date={formated_date}",
        headers={"Authorization": f"Bearer {current_test_token}"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Routines found successfully",
        "routines": [],
    }


@freeze_time(current_date)
def test_endpoint_return_only_not_daily(self_destructible_db, database_populated, client, current_test_token):
    formated_date = (datetime.today() - timedelta(days=4)).strftime("%Y-%m-%d")
    response = client.get(
        f"{route_uri}?date={formated_date}",
        headers={"Authorization": f"Bearer {current_test_token}"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Routines found successfully",
        "routines": [
            {
                "id": 2,
                "title": "ROUTINE 2",
                "qty_done": 2,
                "qty_total": 2,
            },
        ],
    }
