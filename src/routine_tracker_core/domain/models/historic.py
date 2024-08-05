from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from routine_tracker_core.database import RoutineTrackerCoreBaseModel


class Historic(RoutineTrackerCoreBaseModel):
    __tablename__ = "historic"

    id_routine = Column(BigInteger, ForeignKey("routine.id"), index=True, nullable=False)
    id_tracker = Column(BigInteger, ForeignKey("tracker.id"), index=True, nullable=False)
    date = Column(DateTime, server_default=func.now())

    routine = relationship("Routine")
    tracker = relationship("Tracker")
