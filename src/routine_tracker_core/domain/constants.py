from enum import Enum


class PeriodicyEnum(Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    YEARKY = "YEARKY"


class ErrorMessageCodeEnum(Enum):
    USER_NOT_FOUND = "USER_NOT_FOUND"
    INVALID_TOKEN = "INVALID_TOKEN"
