from google.auth.exceptions import GoogleAuthError
from google.auth.transport import requests
from google.oauth2 import id_token

from routine_tracker_core.domain.exceptions import UserInvalidToken


class GoogleOAuthService:
    def verify_token(self, token: str):
        try:
            return id_token.verify_oauth2_token(token, requests.Request())
        except (ValueError, GoogleAuthError):
            raise UserInvalidToken()
