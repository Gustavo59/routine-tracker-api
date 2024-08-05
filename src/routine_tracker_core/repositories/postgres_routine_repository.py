from sqlalchemy import or_

from routine_tracker_core.domain import DailyRoutineDTO, GetDailyRoutineRequestDTO
from routine_tracker_core.domain.models import Frequency, Routine, Tracker
from routine_tracker_core.domain.utils import first_day_of_the_moth, first_day_of_the_week, first_day_of_the_year
from routine_tracker_core.interfaces.repositories import RoutineRepositoryInterface


class PostgresRoutineRepository(RoutineRepositoryInterface):
    def __init__(self, session) -> None:
        self._session = session

    def get_daily_routines(self, get_daily_routine_dto: GetDailyRoutineRequestDTO) -> list[DailyRoutineDTO]:
        routines = (
            self._session.query(
                Routine.id,
                Routine.title,
                Tracker.done,
                Routine.quantity,
            )
            .join(Frequency, Routine.id == Frequency.id_routine, isouter=True)
            .join(Tracker, Routine.id == Tracker.id_routine)
            .filter(Routine.id_user == get_daily_routine_dto.id_user)
            .filter(
                or_(
                    Frequency.day == get_daily_routine_dto.date.weekday(),
                    Frequency.id == None,  # noqa: E711
                ),
                or_(
                    Tracker.date == get_daily_routine_dto.date,
                    Tracker.date == first_day_of_the_week(get_daily_routine_dto.date),
                    Tracker.date == first_day_of_the_moth(get_daily_routine_dto.date),
                    Tracker.date == first_day_of_the_year(get_daily_routine_dto.date),
                ),
            )
            .group_by(Routine.id, Tracker.done)
        ).all()

        return [
            DailyRoutineDTO(
                id=routine.id,
                title=routine.title,
                qty_done=routine.done,
                qty_total=routine.quantity,
            )
            for routine in routines
        ]
