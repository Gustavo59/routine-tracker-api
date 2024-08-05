from datetime import date

import factory
import factory.fuzzy

from routine_tracker_core.domain.models import Frequency


class FrequencyFactory(factory.Factory):
    class Meta:
        model = Frequency

    day = date.today().weekday()

    routine = factory.SubFactory("routine_tracker_core.factories.RoutineFactory")
