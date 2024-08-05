from pydantic import BaseModel


class DailyRoutineDTO(BaseModel):
    id: int
    title: str
    qty_done: int
    qty_total: int
