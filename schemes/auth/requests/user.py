from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import field_validator


class Sign_in(BaseModel):
    email: EmailStr
    password: str


class Sign_up(BaseModel):
    display_name: str
    email: EmailStr
    password: str
    password_confirmation: str

    @field_validator("password_confirmation")
    def password_match(cls, v, info):
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("passwords do not match")
        return v
