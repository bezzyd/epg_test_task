from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
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

    # в тз был указан пункт про обработку пароля, как я понял речь идет про хеширование
    def hash_password(self):
        self.password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
