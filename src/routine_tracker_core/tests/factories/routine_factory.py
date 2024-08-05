import random

import factory

from routine_tracker_core.domain.constants import PeriodicyEnum
from routine_tracker_core.domain.models import Routine


class RoutineFactory(factory.Factory):
    class Meta:
        model = Routine

    title = factory.Sequence(lambda n: "ROUTINE {0}".format(n + 1))
    periodicy = PeriodicyEnum.DAILY
    quantity = random.randint(1, 1000)

    user = factory.SubFactory("routine_tracker_core.factories.UserFactory")
