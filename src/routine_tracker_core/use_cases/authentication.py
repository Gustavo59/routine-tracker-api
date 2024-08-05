from datetime import timedelta

from fastapi_login import LoginManager

from routine_tracker_core.domain import AuthenticateUserDTO, AuthenticateUserRequestDTO
from routine_tracker_core.services import GoogleOAuthService
from routine_tracker_core.settings import get_settings


class Authentication:
    def __init__(self, login_manager: LoginManager, oauth_service: GoogleOAuthService):
        self._login_manager = login_manager
        self._oauth_service = oauth_service

    def run(self, input_dto: AuthenticateUserRequestDTO):
        settings = get_settings()

        session = self._oauth_service.verify_token(token=input_dto.id_token)
        access_token_data = dict(email=session.get("email"), google_token=input_dto.id_token)
        access_token = self._login_manager.create_access_token(
            data=access_token_data,
            expires=timedelta(hours=settings.TOKEN_EXPIRATION_HOURS),
        )
        return AuthenticateUserDTO(access_token=access_token)
