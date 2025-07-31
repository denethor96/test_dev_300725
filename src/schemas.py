from pydantic import BaseModel, EmailStr, field_validator
from typing import List
import re

class Phone(BaseModel):
    number: str
    citycode: str
    contrycode: str

class UserIn(BaseModel):
    name: str
    email: EmailStr
    password: str
    phones: List[Phone]

    @field_validator("password")
    @classmethod
    def password_validator(cls, v):
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=(?:.*\d){2,})[A-Za-z\d]+$'
        if not re.match(pattern, v):
            raise ValueError("La clave debe tener al menos una mayúscula, minúsculas y dos números")
        return v

class UserOut(BaseModel):
    id: str
    name: str
    email: str
    phones: List[Phone]
    created: str
    modified: str
    last_login: str
    token: str
    isactive: bool

class ErrorMessage(BaseModel):
    mensaje: str
