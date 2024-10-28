from pydantic import BaseModel, EmailStr, Field, validator
from typing import List

# список для хранения участников 
participants: List[str] = []


class Participant(BaseModel):
    avatar: str = Field(..., description="URL аватарки")
    gender: str = Field(..., description="Пол участника")
    first_name: str = Field(..., description="Имя участника")
    last_name: str = Field(..., description="Фамилия участника")
    email: EmailStr = Field(..., description="Электронная почта участника")

    @validator('email')
    def check_email_unique(cls, email):
        if email in participants:
            raise ValueError("Email уже используется.")
        return email

    class Config:
        schema_extra = {
            "example": {
                "avatar": "https://masterpiecer-images.s3.yandex.net/4d2ee26774cf11eeaead5696910b1137:upscaled",
                "gender": "male",
                "first_name": "Александр",
                "last_name": "Усенко",
                "email": "usenko.alexandr.work@gmail.com"
            }
        }
