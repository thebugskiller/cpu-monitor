from pydantic import BaseModel, Field


class BaseUser(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=20,
        pattern="^[a-zA-Z0-9]+$",
        description="Alphanumeric username",
    )
    name: str = Field(
        ...,
        min_length=3,
        max_length=75,
        pattern="^[A-Za-z]+(?: [A-Za-z]+)*$",
        description="Full Name (3-75 characters)",
    )


class RegisterUser(BaseUser):
    password: str = Field(..., min_length=6, description="Password (min 6 characters)")
