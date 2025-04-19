import uuid
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID  # Import UUID from uuid module


class User(BaseModel):
    name: str
    emailID: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: Optional[str]
    password: Optional[str]


class UserUpdateOut(BaseModel):
    user_id: UUID  # Correct type for UUID
    name: str
    emailID: EmailStr


class UserOut(BaseModel):
    user_id: UUID  # Correct type for UUID
    name: str
    emailID: EmailStr = Field(alias="email")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True  # Allows using both emailID and email
