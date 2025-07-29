from typing import Optional
from sqlalchemy import Column, VARCHAR, Integer
from sqlmodel import Field, SQLModel, Relationship
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.prompt import Users_prompts

class Mastery_level(Enum):
    JUNIOR_PROMPTER = 1
    MIDDLE_PROMPTER = 2
    SENIOR_PROMPTER = 3
    MILORD_PROMPTER = 4

class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(sa_column=Column(VARCHAR(50), unique=True))
    email: str = Field(sa_column=Column(VARCHAR(100), unique=True))
    password_hash: str = Field(sa_column=Column(VARCHAR(256)))
    level_of_mastery: int = Field(default=1)
    
    
    prompts: list["Users_prompts"] = Relationship(back_populates="user")
    
    
    def verify_password(self, password: str) -> bool:
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    @property
    def password(self):
        raise AttributeError('Password is not readable')

    @password.setter 
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    @classmethod
    def authenticate(cls, session, user_email, password):
        user = session.query(cls).filter(cls.email == user_email).first()
        if user and check_password_hash(user.password_hash, password):
            return user
        return None