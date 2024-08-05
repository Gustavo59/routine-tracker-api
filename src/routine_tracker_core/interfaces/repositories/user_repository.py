from abc import ABC, abstractmethod

from routine_tracker_core.domain.models import User


class UserRepositoryInterface(ABC):
    @abstractmethod
    def create_and_flush(self, email: str) -> User:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> User:
        pass
