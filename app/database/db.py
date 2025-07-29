import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from typing import Optional
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, VARCHAR, Integer, DateTime, func
from sqlmodel import Field, SQLModel, Relationship, create_engine
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app.models import Users_prompts

def initialize_database():
    engine = create_engine("sqlite:///app/database/database.db")
    SQLModel.metadata.create_all(engine)
    print("Базу даних та таблиці успішно створено!")

if __name__ == "__main__":
    initialize_database()