from routine_tracker_core.domain.exceptions import UserNotFound
from routine_tracker_core.domain.models import User
from routine_tracker_core.interfaces.repositories import UserRepositoryInterface


class PostgresUserRepository(UserRepositoryInterface):
    def __init__(self, session) -> None:
        self._session = session

    def create_and_flush(self, email: str) -> User:
        user = User(email=email)
        self._session.add(user)
        self._session.flush()
        return user

    def find_by_email(self, email: str) -> User:
        user = self._session.query(User).filter(User.email == email).one_or_none()
        if not user:
            raise UserNotFound
        return user
