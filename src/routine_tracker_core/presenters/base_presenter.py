from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from routine_tracker_core.domain.exceptions import RoutineTrackerCoreBaseException
from routine_tracker_core.interfaces.presenters.base_presenter import BasePresenterInterface


class BasePresenter(BasePresenterInterface):
    def present_field_required(self, exc: ValidationError) -> JSONResponse:
        """Present missing field required

        Args:
            exc (ValidationError): Pydantic error

        Returns:
            JSONResponse: JSONResponse
        """
        missing_fields = []
        invalid_fields = {}
        for e in exc.errors():
            if e["type"] == "missing":
                missing_fields.append(".".join(e["loc"]))
            else:
                invalid_fields.update({".".join(e["loc"]): e["msg"]})

        return JSONResponse(
            content={
                "message": "Validation error on request body",
                "missing_fields": missing_fields,
                "invalid_fields": invalid_fields,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    def present_with_error(self, err) -> JSONResponse:
        """Present with error

        Args:
            err (Any): Error of any type

        Raises:
            err: Exception

        Returns:
            JSONResponse: JSONResponse
        """
        if isinstance(err, RoutineTrackerCoreBaseException) and err.http_status < 500:
            return JSONResponse(content={"message": err.message}, status_code=err.http_status)
        raise err
