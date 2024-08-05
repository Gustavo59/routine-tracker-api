from fastapi import status
from fastapi.responses import JSONResponse

from routine_tracker_core.domain import DailyRoutineDTO
from routine_tracker_core.interfaces.presenters import RoutinePresenterInterface
from routine_tracker_core.presenters.base_presenter import BasePresenter


class RoutinePresenter(RoutinePresenterInterface, BasePresenter):
    def present_found(self, routines: list[DailyRoutineDTO]) -> JSONResponse:
        routines = [routine.model_dump() for routine in routines]
        return JSONResponse(
            content={"message": "Routines found successfully", "routines": routines},
            status_code=status.HTTP_200_OK,
        )
