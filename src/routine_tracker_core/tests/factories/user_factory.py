import factory

from routine_tracker_core.domain.models import User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: "user_{0}@email.com".format(n + 1))
