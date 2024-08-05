from routine_tracker_core.domain import DailyRoutineDTO, GetDailyRoutineRequestDTO
from routine_tracker_core.interfaces.repositories import RoutineRepositoryInterface


class GetDailyRoutine:
    def __init__(self, routine_repository: RoutineRepositoryInterface):
        self._routine_repository = routine_repository

    def run(self, input_dto: GetDailyRoutineRequestDTO) -> list[DailyRoutineDTO]:
        try:
            return self._routine_repository.get_daily_routines(get_daily_routine_dto=input_dto)
        except Exception as e:
            raise e
