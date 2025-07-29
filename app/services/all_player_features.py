from sqlmodel import Session, select
from app.models import User, Users_prompts
from app.controllers import UserController
from app.services.prompt_mark_settings import calculate_prompt_quality 
import random
from typing import List, Tuple

def duel_with_friend():
    """    
    Два користувача по черзі вводять свої промти,
    після чого вони оцінюються за допомогою фукнції evaluate_prompt_quality.
    Користувач з найбільшою оцінкою виграє і отримає бал 
    Гра йде до 3 балів 
    """
    print("Починаємо гру 'Дуель з другом'!")

    user1_score = 0
    user2_score = 0

    while user1_score < 3 or user2_score < 3:
        print("Раунд починається!")
        topic_category = input("Введіть категорію (Навчання, Творчість, Програмування): ")
        if topic_category not in ["Навчання", "Творчість", "Програмування"]:
            print("Невірна категорія. Спробуйте ще раз.")
            continue
        print(f"Категорія: {topic_category}")
        print("Кожен користувач по черзі вводить свій промт.")
        print("Початок раунду! Удачі!")
        
        user1_prompt = input("Користувач 1, введіть ваш промт: ")
        user2_prompt = input("Користувач 2, введіть ваш промт: ")

        user1_quality = calculate_prompt_quality(user1_prompt, topic_category)
        user2_quality = calculate_prompt_quality(user2_prompt, topic_category)

        print(f"Користувач 1 отримав {user1_quality} балів.")
        print(f"Користувач 2 отримав {user2_quality} балів.")

        if user1_quality > user2_quality:
            user1_score += 1
            print("Користувач 1 виграв раунд!")
        elif user2_quality > user1_quality:
            user2_score += 1
            print("Користувач 2 виграв раунд!")
        else:
            print("Нічия!")

    if user1_score == 3:
        print("Користувач 1 виграв гру!")
    else:
        print("Користувач 2 виграв гру!")




def display_user_prompts(user_id: int, session: Session) -> List[Users_prompts]:
    """
    Функція для відображення всіх промтів користувача.
    :param user_id: ID користувача
    :return: Список промтів користувача
    """
    user = session.get(User, user_id)
    if not user:
        raise ValueError("User not found")

    prompts = session.query(Users_prompts).filter(Users_prompts.user_id == user_id).all()
    return prompts






def get_prompt_pairs() -> List[Tuple[str, str, bool]]:
    """
    Returns a list of tuples containing pairs of prompts (good and bad) with descriptions.
    Each tuple contains: (prompt text, explanation, is_good_prompt)
    """
    prompt_pairs = [
    (
        "Створіть функцію на Python, яка сортує список чисел за зростанням використовуючи алгоритм bubble sort. Додайте коментарі для пояснення кожного кроку та оцініть складність алгоритму.",
        "Чіткий промпт: вказано мову, алгоритм, вимоги до документації та додаткові вимоги щодо коментарів",
        True
    ),
    (
        "Напишіть код який щось сортує",
        "Розмитий промпт: не вказано мову, тип даних, метод сортування та інші важливі деталі",
        False
    ),
    (
        "Реалізуйте функцію на JavaScript для фільтрації масиву об'єктів за заданими критеріями (ім'я, вік, стать) з можливістю сортування за будь-яким полем. Експортуйте функцію як модуль.",
        "Чіткий промпт: визначено мову, тип даних, функціональні вимоги та вимоги до архітектури",
        True
    ),
    (
        "Зроби фільтр для масиву",
        "Розмитий промпт: відсутні деталі реалізації, мова, критерії фільтрації",
        False
    ),
    (
        "Напишіть SQL-запит для отримання середньої зарплати по кожному відділу компанії, враховуючи лише працівників зі стажем більше 3 років. Відсортуйте результати за спаданням зарплати.",
        "Чіткий промпт: чітко визначена мета запиту, умови фільтрації та сортування",
        True
    ),
    (
        "Дістати дані про зарплати",
        "Розмитий промпт: не визначено мову, джерело даних, умови відбору чи обробки",
        False
    ),
    (
        "Створіть REST API на Node.js з використанням Express, яке надає CRUD операції для ресурсу 'Користувачі'. Використовуйте MongoDB як базу даних. Додайте валідацію вхідних даних та JWT аутентифікацію.",
        "Чіткий промпт: визначено стек технологій, функціональні вимоги та вимоги безпеки",
        True
    ),
    (
        "Зроби API для користувачів",
        "Розмитий промпт: відсутні деталі реалізації, технології, вимоги до функціоналу",
        False
    ),
    (
        "Напишіть unit-тести на Python з використанням pytest для функції, яка обчислює факторіал числа. Перевірте крайні випадки (0, 1, від'ємні числа) та типізацію даних.",
        "Чіткий промпт: визначено фреймворк, об'єкт тестування та конкретні тест-кейси",
        True
    ),
    (
        "Протестуй функцію",
        "Розмитий промпт: не вказано що тестувати, які випадки, який фреймворк",
        False
    )
]
    return prompt_pairs

def prompt_game(required_correct: int = 3) -> None:
    """
    Гра для вгадування якісних промптів
    
    Args:
        required_correct: кількість правильних відповідей для перемоги
    """
    correct_answers = 0
    used_prompts = set()
    prompt_pairs = get_prompt_pairs()
    
    print("\nВітаємо в грі 'Знавець промптів'!")
    print(f"Вгадайте {required_correct} хороших промптів для перемоги.\n")
    
    while correct_answers < required_correct:
        
        available_pairs = [p for p in prompt_pairs if p[0] not in used_prompts]
        if not available_pairs:
            used_prompts.clear()
            available_pairs = prompt_pairs
            
        pair = random.choice(available_pairs)
        prompt, explanation, is_good = pair
        used_prompts.add(prompt)
        
        print("\n" + "="*50)
        print("Оцініть цей промпт:")
        print(f"\n{prompt}\n")
        print("Це хороший промпт? (так/ні)")
        
        answer = input(">>> ").lower().strip()
        is_yes = answer in ['так', 'y', 'yes', 'т']
        
        if (is_yes and is_good) or (not is_yes and not is_good):
            correct_answers += 1
            print(f"\nПравильно! {explanation}")
            print(f"Правильних відповідей: {correct_answers}/{required_correct}")
        else:
            print(f"\nНа жаль, це неправильно. {explanation}")
            print("Спробуйте спочатку!")
            correct_answers = 0
            
    print("\nВітаємо! Ви успішно завершили гру!")
    
    
    
    
    
    
    
def show_user_prompts(session: Session, user_id: int):
    """Показує всі промпти користувача"""
    prompts = UserController.get_user_prompts(session, user_id)
    if not prompts:
        print("У вас поки немає збережених промптів")
        return
        
    print("\nВаші промпти:")
    for i, prompt in enumerate(prompts, 1):
        print(f"{i}. {prompt.text} (створено: {prompt.created_at})")

def show_leaderboard(session: Session):
    users = session.query(User).order_by(User.level_of_mastery.desc()).limit(10).all()
    
    if not users:
        print("\nПоки що немає користувачів у таблиці лідерів")
        return
        
    print("\nТаблиця лідерів:")
    print("Ранг | Користувач | Рівень майстерності")
    print("-" * 40)
    
    for rank, user in enumerate(users, 1):
        print(f"{rank:4} | {user.username:10} | {user.level_of_mastery}")