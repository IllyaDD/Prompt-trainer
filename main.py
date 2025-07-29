import logging
import sys
from typing import Optional, Tuple
from sqlmodel import Session, create_engine, SQLModel
from app.controllers.user import UserController
from app.models.user import User
from app.services import (
    calculate_prompt_quality,
    examples,
    hints,
    duel_with_friend,
    prompt_game,
    show_leaderboard,
    show_user_prompts
)
from app.services.menu_handlers import handle_prompt_evaluation
from sqlalchemy import select
from sqlalchemy.orm import Session
engine = create_engine("sqlite:///app/database/database.db")




def some_lines():
    print("-"*20)

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer)


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)  
    ]
)

def register_user(session: Session) -> Tuple[str, str, str]:
    """
    Реєстрація нового користувача з верифікацією email
    
    Повертає:
        tuple: (username, email, password)
    """
    logging.info("Початок процесу реєстрації")
    
    try:
        username = input(">>> Введіть ім'я користувача: ").strip()
        email = input(">>> Введіть електронну пошту: ").strip()
        password = input(">>> Введіть пароль: ").strip()

        if not all([username, email, password]):
            print("Усі поля повинні бути заповнені")
            return register_user(session)

        try:
            user = UserController.create_user(session, username, email, password)
            print(f"Користувач {username} успішно зареєстрований")
            return username, email, password
        except ValueError as e:
            print(f"Помилка: {str(e)}")
            return register_user(session)
            
    except Exception as e:
        logging.error(f"Помилка реєстрації: {str(e)}")
        print("Виникла помилка при реєстрації. Спробуйте ще раз")
        return register_user(session)

def login_user(session: Session, max_attempts: int = 3) -> Optional[User]:
    """
    Авторизація користувача з обмеженою кількістю спроб
    
    Args:
        session: SQLAlchemy сесія
        max_attempts: максимальна кількість спроб входу
        
    Returns:
        Optional[User]: об'єкт користувача або None при невдачі
    """
    attempts = 0
    while attempts < max_attempts:
        attempts += 1
        remaining = max_attempts - attempts
        
        logging.info("Початок процесу авторизації")
        try:
            email = input(">>> Введіть електронну пошту: ").strip()
            password = input(">>> Введіть пароль: ").strip()
            
            user = UserController.authenticate_user(session, email, password)
            
            if user:
                print(f"Вітаємо, {user.username}!")
                return user
            else:
                logging.warning("Невірні облікові дані")
                if remaining > 0:
                    print(f"Невірний email або пароль. Залишилось спроб: {remaining}")
                else:
                    print("Перевищено кількість спроб входу. Поверніться пізніше.")
                    
        except Exception as e:
            logging.error(f"Помилка авторизації: {str(e)}")
            return None
            
    return None








def menu(session: Session, current_user: User):
    while True:
        some_lines()
        print(f"Вітаємо в нашому тренажері з промтів, {current_user.username}!")
        some_lines()
        print("1. Поради для створення промтів")
        print("2. Тренажер промтів")
        print("3. Дуель з другом")
        print("4. Мої промпти")
        print("5. Таблиця лідерів")
        print("6. Вийти")
        menu_answer = input(">>> Введіть номер пункту меню: ")
        
        if menu_answer == "1":
            examples()
            input("Натисніть Enter для повернення в меню...")
        elif menu_answer == "2":
            training_menu(session, current_user)
        elif menu_answer == "3":
            duel_with_friend()
            input("Натисніть Enter для повернення в меню...")
        elif menu_answer == "4":
            show_user_prompts(session, current_user.id)
            input("Натисніть Enter для повернення в меню...")
        elif menu_answer == "5":
            show_leaderboard(session)
            input("Натисніть Enter для повернення в меню...")
        elif menu_answer == "6":
            exit_program()
def menu_registration(session: Session):
    while True:
        some_lines()
        print("""
Вітаємо в меню реєстрації!
1. Зареєструватися
2. Увійти в акаунт
3. Вийти
        """)
        some_lines()
        registration_answer = input(">>> Введіть номер пункту меню: ")
        
        if registration_answer == "1":
            result = register_user(session)
            if result:
                user = UserController.authenticate_user(session, result[1], result[2])
                if user:
                    menu(session, user)
                    break
        elif registration_answer == "2":
            user = login_user(session)
            if user:  
                menu(session, user)
                break
        elif registration_answer == "3":
            exit_program()
            
            
def exit_program():
    print("Дякуємо за використання нашого тренажеру!")
    exit(0)
        

def start_training(session: Session, current_user: User):
    """
    Тренування створення промтів з вибором категорії
    
    Args:
        session: SQLAlchemy сесія
        current_user: поточний користувач
    """
    while True:
        print("""
        Виберіть категорію для тренування:
        1. Навчання
        2. Творчість
        3. Програмування
        4. Повернутися назад
        """)
        category_choice = input(">>> Введіть номер категорії: ")
        
        if category_choice in ["1", "2", "3"]:
            categories = {
                "1": "Навчання",
                "2": "Творчість", 
                "3": "Програмування"
            }
            category = categories[category_choice]
            print(f"Ви обрали категорію '{category}'")
            input_text = input("Введіть ваш промт: ")
            
            quality = calculate_prompt_quality(input_text, category)
            print(f"Якість вашого промту: {quality}/10")
            
            
            UserController.save_prompt(session, current_user.id, input_text)
            
            
            if quality >= 8:
                UserController.raise_mastery_level(session, current_user.id)
                
            input("Натисніть Enter для продовження...")
        elif category_choice == "4":
            return
        else:
            print("Невірний вибір. Спробуйте ще раз.")


        
def training_menu(session: Session, current_user: User):
    print("""
        Вітаємо в тренажері промтів!
        1. Тренажер промтів
        2. Поради для створення промтів
        3. Гра "Вгадай промт"
        4. Повернутися в головне меню
        """)
    while True:
        training_choice = input(">>> Введіть номер пункту меню: ")
        if training_choice == "1":
            start_training(session, current_user)
        elif training_choice == "2":
            hints()
            input("Натисніть Enter для продовження...")
        elif training_choice == "3":
            prompt_game()
            input("Натисніть Enter для продовження...")
        elif training_choice == "4":
            return
        else:
            print("Невірний вибір. Спробуйте ще раз.")









if __name__ == "__main__":
    SQLModel.metadata.create_all(engine)
    logging.info("Program started")
    
    with Session(engine) as session:
        menu_registration(session)