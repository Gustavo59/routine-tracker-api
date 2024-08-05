from abc import ABC, abstractmethod

from fastapi.responses import JSONResponse
from pydantic import ValidationError


class BasePresenterInterface(ABC):
    @abstractmethod
    def present_field_required(self, exc: ValidationError) -> JSONResponse:
        """Present missing field required

        Args:
            error (_type_): Pydantic error

        Returns:
            JSONResponse: JSONResponse
        """
        pass

    @abstractmethod
    def present_with_error(self, err) -> JSONResponse:
        """Present with error

        Args:
            err (Any): Error of any type

        Raises:
            err: Exception

        Returns:
            JSONResponse: JSONResponse
        """
        pass
