from fastapi import status
from fastapi.responses import JSONResponse

from routine_tracker_core.domain import AuthenticateUserRequestDTO
from routine_tracker_core.presenters.base_presenter import BasePresenter


class AuthenticationPresenter(BasePresenter):
    def present_valid_token(self, output_dto: AuthenticateUserRequestDTO) -> JSONResponse:
        """Present with valid token

        Args:
            token (AuthenticateUserRequestDTO): AuthenticateUserRequestDTO

        Returns:
            JSONResponse: JSONResponse
        """
        return JSONResponse(
            content={
                "message": "User authenticated successfully",
                "token": output_dto.access_token,
            },
            status_code=status.HTTP_200_OK,
        )

    def present_with_invalid_token(self) -> JSONResponse:
        """Present invalid token message

        Returns:
            JSONResponse: JSONResponse
        """
        return JSONResponse(
            content={"message": "Invalid token"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
