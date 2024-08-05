from routine_tracker_core.domain.constants import ErrorMessageCodeEnum


class RoutineTrackerCoreBaseException(Exception):
    message = None
    http_status = 500

    def __init__(self, message=None, http_status=None, *args):
        self.message = message or self.message
        self.http_status = http_status or self.http_status
        super().__init__(self.message, *args)


class UserNotFound(RoutineTrackerCoreBaseException):
    message = ErrorMessageCodeEnum.USER_NOT_FOUND.value
    http_status = 404


class UserInvalidToken(RoutineTrackerCoreBaseException):
    message = ErrorMessageCodeEnum.INVALID_TOKEN.value
    http_status = 403
