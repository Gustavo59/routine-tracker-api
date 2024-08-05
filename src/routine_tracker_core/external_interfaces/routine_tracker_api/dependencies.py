import logging

import jwt
from fastapi import FastAPI, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_login import LoginManager
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from routine_tracker_core.controllers import AuthenticationController
from routine_tracker_core.settings import get_settings

LOGGER = logging.getLogger(__name__)

settings = get_settings()

login_manager = LoginManager(settings.JWT_SECRET.get_secret_value(), "/auth")


def app_factory(title: str = "FastAPI"):
    allow_origins = ["*"]

    init_config = dict(
        middleware=[
            Middleware(
                CORSMiddleware,
                allow_origins=allow_origins,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=[
                    "Origin",
                    "X-Origin",
                    "Access-Control-Request-Method",
                    "Access-Control-Request-Headers",
                    "X-Access-Control-Request-Method",
                    "X-Access-Control-Request-Headers",
                    "Authorization",
                ],
                expose_headers=[
                    "Origin",
                    "X-Origin",
                    "Access-Control-Request-Method",
                    "Access-Control-Request-Headers",
                    "X-Access-Control-Request-Method",
                    "X-Access-Control-Request-Headers",
                    "Authorization",
                ],
            )
        ]
    )

    app = FastAPI(**init_config, title=title)
    return app


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        try:
            credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
            if credentials:
                if not credentials.scheme == "Bearer":
                    raise HTTPException(status_code=403, detail="Invalid authentication scheme.")

                is_token_valid, id_user = self.verify_jwt(credentials.credentials)
                if not is_token_valid:
                    raise HTTPException(status_code=403, detail="Invalid or expired token")

                return dict(id_user=id_user)
        except Exception as exc:
            LOGGER.error(f"Error to decode token in Routine Tracker API {exc}")
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, token: str):
        from routine_tracker_core.settings import get_settings

        jwt_secret = get_settings().JWT_SECRET.get_secret_value()
        payload = jwt.decode(token, jwt_secret, algorithms=["HS256"])
        authentication_controller = AuthenticationController(None)
        is_token_valid, id_user = authentication_controller.validate_jwt(
            expiration_date=payload["exp"], email=payload["email"]
        )
        return is_token_valid, id_user
