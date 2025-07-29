from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class Users_prompts(SQLModel, table=True):
    __tablename__ = "users_prompts"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    text: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    user: user = Relationship(back_populates="prompts")