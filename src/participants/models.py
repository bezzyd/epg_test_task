from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator
import bcrypt

# список для хранения участников
participants: list[dict] = []


class Participant(BaseModel):
    id: int = Field(..., description="id")
    avatar: str = Field(..., description="avatar url")
    gender: str = Field(..., description="gender")
    first_name: str = Field(..., description="first name")
    last_name: str = Field(..., description="last name")
    email: EmailStr = Field(..., description="email")
    password: str = Field(..., description="password")
    registration_date: datetime = Field(default_factory=datetime.utcnow)
    latitude: float = Field(..., description="latitude")
    longitude: float = Field(..., description="longitude")

    @field_validator('latitude')
    @classmethod
    def check_latitude(cls, v):
        if not (-90 <= v <= 90):
            raise ValueError('latitude must be between -90 and 90')
        return v

    @field_validator('longitude')
    @classmethod
    def check_longitude(cls, v):
        if not (-180 <= v <= 180):
            raise ValueError('longitude must be between -180 and 180')
        return v

    # в тз был указан пункт про обработку пароля, как я понял речь идет про хеширование
    def hash_password(self):
        self.password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
