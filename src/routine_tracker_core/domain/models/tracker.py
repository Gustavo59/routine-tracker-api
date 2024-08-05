from sqlalchemy import BigInteger, Column, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship

from routine_tracker_core.database import RoutineTrackerCoreBaseModel


class Tracker(RoutineTrackerCoreBaseModel):
    __tablename__ = "tracker"

    id_routine = Column(BigInteger, ForeignKey("routine.id"), index=True, nullable=False)
    date = Column(Date, nullable=False)
    done = Column(Integer, nullable=False, server_default="0")

    routine = relationship("Routine")
