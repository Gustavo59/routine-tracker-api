from datetime import date

from pydantic import ValidationError

from routine_tracker_core.database import session_scope
from routine_tracker_core.domain import GetDailyRoutineRequestDTO
from routine_tracker_core.presenters import RoutinePresenter
from routine_tracker_core.repositories import PostgresRoutineRepository
from routine_tracker_core.use_cases import GetDailyRoutine


class RoutineController:
    def __init__(self):
        self._presenter = RoutinePresenter()

    def get_daily_routines(self, id_user: int, date: date = None):
        with session_scope() as session:
            routine_repository = PostgresRoutineRepository(session)

            try:
                get_daily_routine_dto = GetDailyRoutineRequestDTO(id_user=id_user, date=date)

                use_case = GetDailyRoutine(routine_repository=routine_repository)
                routines = use_case.run(input_dto=get_daily_routine_dto)
            except ValidationError as exc:
                return self._presenter.present_field_required(exc)
            except Exception as exc:
                raise self._presenter.present_with_error(exc)

        return self._presenter.present_found(routines=routines)
