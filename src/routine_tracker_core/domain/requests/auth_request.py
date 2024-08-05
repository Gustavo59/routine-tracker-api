from pydantic import BaseModel


class AuthenticateUserRequestDTO(BaseModel):
    id_token: str
