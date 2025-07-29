from datetime import datetime
from typing import Optional
from sqlalchemy import Column, DateTime, VARCHAR, Integer, func
from sqlmodel import Field, SQLModel, Relationship

class Users_prompts(SQLModel, table=True):
    """
    Модель для збереження промтів користувача.
    """
    __tablename__ = "users_prompts"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")  # Changed from "user.id" to "users.id"
    text: str = Field(sa_column=Column(VARCHAR(500)))
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, default=func.now())
    )

    user: "User" = Relationship(back_populates="prompts")