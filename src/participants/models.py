from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List
import bcrypt

# список для хранения участников 
participants: List[dict] = []


class Participant(BaseModel):
    avatar: str = Field(..., description="avatar url")
    gender: str = Field(..., description="gender")
    first_name: str = Field(..., description="first name")
    last_name: str = Field(..., description="last name")
    email: EmailStr = Field(..., description="email")
    password: str = Field(..., description="password")

    # проверка уникальности почты
    @field_validator('email')
    def check_email_unique(cls, email):
        if any(participant['email'] == email for participant in participants):
            raise ValueError("email already registered")
        return email

    # в тз был указан пункт про обработку пароля, как я понял речь идет про хеширование
    def hash_password(self):
        self.password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
