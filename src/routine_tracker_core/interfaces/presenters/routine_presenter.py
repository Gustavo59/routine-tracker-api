from abc import abstractmethod

from fastapi.responses import JSONResponse

from routine_tracker_core.domain import DailyRoutineDTO
from routine_tracker_core.interfaces.presenters.base_presenter import BasePresenterInterface


class RoutinePresenterInterface(BasePresenterInterface):
    @abstractmethod
    def present_found(self, routines: list[DailyRoutineDTO]) -> JSONResponse:
        pass
