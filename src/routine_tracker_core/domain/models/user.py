from sqlalchemy import Column, String

from routine_tracker_core.database import RoutineTrackerCoreBaseModel


class User(RoutineTrackerCoreBaseModel):
    __tablename__ = "user"

    email = Column(String, nullable=False, unique=True)
