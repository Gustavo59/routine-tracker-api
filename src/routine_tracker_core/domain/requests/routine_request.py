from datetime import date

from pydantic import BaseModel


class GetDailyRoutineRequestDTO(BaseModel):
    id_user: int
    date: date
