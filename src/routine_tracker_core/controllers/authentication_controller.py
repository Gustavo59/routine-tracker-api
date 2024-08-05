import logging
import time

from fastapi_login import LoginManager

from routine_tracker_core.database import session_scope
from routine_tracker_core.domain import AuthenticateUserRequestDTO
from routine_tracker_core.domain.exceptions import UserInvalidToken, UserNotFound
from routine_tracker_core.presenters import AuthenticationPresenter
from routine_tracker_core.repositories import PostgresUserRepository
from routine_tracker_core.services import GoogleOAuthService
from routine_tracker_core.use_cases import Authentication

LOGGER = logging.getLogger(__name__)


class AuthenticationController:
    def __init__(self, login_manager: LoginManager):
        self._login_manager = login_manager
        self._presenter = AuthenticationPresenter()

    def authenticate(self, request: dict):
        try:
            authenticate_user_dto = AuthenticateUserRequestDTO(**request)
            use_case = Authentication(login_manager=self._login_manager, oauth_service=GoogleOAuthService())
            output_dto = use_case.run(input_dto=authenticate_user_dto)
            return self._presenter.present_valid_token(output_dto=output_dto)
        except UserInvalidToken:
            return self._presenter.present_with_invalid_token()
        except Exception as exc:
            LOGGER.exception(exc)
            return self._presenter.present_with_error(message="Unexpected erro while authenticating user")

    def validate_jwt(self, *, expiration_date: int, email: str):
        with session_scope() as session:
            repo = PostgresUserRepository(session)
            try:
                user = repo.find_by_email(email)
            except UserNotFound:
                user = repo.create_and_flush(email=email)
        return expiration_date >= time.time(), user.id
