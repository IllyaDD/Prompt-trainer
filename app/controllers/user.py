# -*- coding: utf-8 -*-
from requests import session
from app.models.user import User, Mastery_level
from sqlmodel import Session, select
from typing import Optional
from app.models import Users_prompts
import datetime
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import Session as AlchemySession
from sqlalchemy import select as sa_select
import logging

class UserController:
    @staticmethod
    def create_user(session: Session, username: str, email: str, password: str) -> User:
    
        existing_user = session.query(User).filter(
            (User.email == email) | (User.username == username)
        ).first()
        
        if existing_user:
            if existing_user.email == email:
                raise ValueError("Email вже використовується")
            else:
                raise ValueError("Ім'я користувача вже зайняте")

        new_user = User(
            username=username,
            email=email,
            level_of_mastery=1
        )
        new_user.password = password
        
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        
        return new_user
    
    @staticmethod
    def delete_user(session: Session, user_id: int) -> None:
        user = session.get(User, user_id)
        if user:
            session.delete(user)
            session.commit()
        else:
            raise ValueError("User not found")
    
    @staticmethod
    def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        try:
            
            user = session.query(User).filter(User.email == email).first()
            if user and user.verify_password(password):
                return user
            return None
        except Exception as e:
            logging.error(f"Authentication error: {str(e)}")
            return None
    
    @staticmethod
    def raise_mastery_level(session: Session, user_id: int) -> User:
        user = session.get(User, user_id)
        if not user:
            raise ValueError("User not found")
        
        if user.level_of_mastery < 4:
            user.level_of_mastery += 1
            session.commit()
            session.refresh(user)
        return user
    
    @staticmethod
    def save_prompt(session: Session, user_id: int, prompt_text: str) -> None:
        user = session.get(User, user_id)
        if not user:
            raise ValueError("User not found")
        
        new_prompt = Users_prompts(user_id=user_id, text=prompt_text, created_at=datetime.datetime.utcnow())
        session.add(new_prompt)
        session.commit()
        
    @staticmethod
    def get_user_prompts(session: Session, user_id: int) -> list[Users_prompts]:
        user = session.get(User, user_id)
        if not user:
            raise ValueError("User not found")
        
        prompts = session.query(select(Users_prompts).where(Users_prompts.user_id == user_id)).all()
        return prompts

    @staticmethod
    def get_user_prompts(session: Session, user_id: int) -> list[Users_prompts]:
        user = session.get(User, user_id)
        if not user:
            raise ValueError("User not found")
        
        
        prompts = session.query(Users_prompts).filter(Users_prompts.user_id == user_id).all()
        return prompts