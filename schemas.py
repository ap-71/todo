from pydantic import BaseModel
from db import get_session
from models import Base, User
from utils import generate_password_hash


class UserSchema(BaseModel):
    id: int
    username: str
    description: str | None = None


class TaskCreateSchema(BaseModel):
    title: str
    description: str

class TaskSchema(TaskCreateSchema):
    id: int

class LoginSchema(BaseModel):
    login: str
    password: str

    def check_login(self):
        user = self.get_user()

        return user is not None

    def get_user(self) -> UserSchema | None:
        with get_session() as session:
            password_hash = generate_password_hash(self.password)
            user = session.query(User).filter_by(username=self.login).first()

            if user is None:
                new_user = User(username=self.login, password=password_hash)
                session.add(new_user)
                session.commit()

                user = new_user
            elif user.password != password_hash:
                return None

            return UserSchema(id=user.id, username=user.username, description=user.description)
