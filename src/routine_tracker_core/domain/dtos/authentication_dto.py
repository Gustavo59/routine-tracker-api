from pydantic import BaseModel


class AuthenticateUserDTO(BaseModel):
    access_token: str
