from abc import ABC, abstractmethod

from routine_tracker_core.domain import DailyRoutineDTO, GetDailyRoutineRequestDTO


class RoutineRepositoryInterface(ABC):
    @abstractmethod
    def get_daily_routines(self, get_daily_routine_dto: GetDailyRoutineRequestDTO) -> list[DailyRoutineDTO]:
        pass
