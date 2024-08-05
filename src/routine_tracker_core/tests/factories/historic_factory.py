from datetime import date, timedelta

import factory
import factory.fuzzy

from routine_tracker_core.domain.models import Historic


class HistoricFactory(factory.Factory):
    class Meta:
        model = Historic

    date = factory.Faker(
        "date_between_dates",
        date_start=date.today() - timedelta(days=date.today().weekday()),
        date_end=date.today() - timedelta(days=date.today().weekday()) + timedelta(days=6),
    )

    routine = factory.SubFactory("routine_tracker_core.factories.RoutineFactory")
    tracker = factory.SubFactory("routine_tracker_core.factories.TrackerFactory")
