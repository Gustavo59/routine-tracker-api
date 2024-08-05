from sqlalchemy import BigInteger, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from routine_tracker_core.database import RoutineTrackerCoreBaseModel


class Frequency(RoutineTrackerCoreBaseModel):
    __tablename__ = "frequency"

    id_routine = Column(BigInteger, ForeignKey("routine.id"), index=True, nullable=False)
    day = Column(Integer, nullable=False)

    routine = relationship("Routine")
