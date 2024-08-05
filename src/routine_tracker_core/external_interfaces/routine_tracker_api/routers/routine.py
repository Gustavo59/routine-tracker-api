from datetime import date

from fastapi import APIRouter, Depends, Response

from routine_tracker_core.controllers import RoutineController
from routine_tracker_core.external_interfaces.routine_tracker_api.dependencies import JWTBearer

router = APIRouter(prefix="/routine", tags=["Routine"])


@router.get("/daily", response_class=Response)
def get_daily_routines(date: date = None, dependencies=Depends(JWTBearer())):
    controller = RoutineController()
    return controller.get_daily_routines(date=date, id_user=dependencies.get("id_user"))
