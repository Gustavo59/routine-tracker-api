from contextlib import contextmanager
from functools import lru_cache
from sqlite3 import DatabaseError

from sqlalchemy import BigInteger, Column, NullPool, create_engine
from sqlalchemy.orm import as_declarative, sessionmaker
from sqlalchemy.sql.schema import MetaData

from routine_tracker_core.settings import get_settings

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=naming_convention)


@as_declarative(metadata=metadata)
class SQLAlchemyBaseModel:
    pass


class RoutineTrackerCoreBaseModel(SQLAlchemyBaseModel):
    __abstract__ = True

    id = Column(BigInteger, primary_key=True)


@lru_cache
def get_engine():
    settings = get_settings()
    return create_engine(str(settings.DATABASE_URL), poolclass=NullPool)


@contextmanager
def session_scope():
    engine = get_engine()
    with SessionLocal(bind=engine) as session:
        yield session
        try:
            session.commit()
        except DatabaseError as err:
            session.rollback()
            raise err
