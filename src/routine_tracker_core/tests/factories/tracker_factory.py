import factory
import factory.fuzzy

from routine_tracker_core.domain.models import Tracker


class TrackerFactory(factory.Factory):
    class Meta:
        model = Tracker

    routine = factory.SubFactory("routine_tracker_core.factories.RoutineFactory")
