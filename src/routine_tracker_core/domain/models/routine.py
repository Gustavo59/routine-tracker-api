from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

from routine_tracker_core.database import RoutineTrackerCoreBaseModel
from routine_tracker_core.domain.constants import PeriodicyEnum


class Routine(RoutineTrackerCoreBaseModel):
    __tablename__ = "routine"

    title = Column(String, nullable=False)
    periodicy = Column(ENUM(PeriodicyEnum), nullable=False)
    quantity = Column(Integer, nullable=False)
    id_user = Column(BigInteger, ForeignKey("user.id"), index=True, nullable=False)

    user = relationship("User")
