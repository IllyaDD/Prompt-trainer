from app.controllers import UserController

mode_keywords = {
    "Програмування": [
        "код", "функція", "клас", "метод", "алгоритм",
        "оптимізація", "дебаг", "тестування", "рефакторинг", "архітектура",
        "патерн", "фреймворк", "бібліотека", "api", "база даних",
        "змінна", "цикл", "умова", "масив", "об'єкт"
    ],
    "Навчання": [
        "поясни", "навчи", "розкажи", "опиши", "допоможи",
        "приклад", "концепція", "теорія", "практика", "завдання",
        "методика", "алгоритм", "структура", "визначення", "термін",
        "урок", "тема", "матеріал", "знання", "розуміння"
    ],
    "Творчість": [
        "створи", "придумай", "намалюй", "опиши", "уяви",
        "креативний", "оригінальний", "незвичайний", "художній", "творчий",
        "натхнення", "ідея", "концепт", "дизайн", "стиль",
        "фантазія", "образ", "композиція", "колір", "форма"
    ]
}

def calculate_prompt_quality(prompt_text: str, prompt_tema: str) -> int:
    if prompt_tema not in mode_keywords:
        raise KeyError(f"Невідома категорія: {prompt_tema}. Доступні категорії: {', '.join(mode_keywords.keys())}")
        
    words = prompt_text.lower().split()
    score = 0
    
    
    if 5 <= len(words) <= 50:
        score += 2
    
    
    keywords_found = sum(1 for word in words if word in mode_keywords[prompt_tema])
    score += min(keywords_found * 2, 4)
    
    
    if any(word in words for word in ["конкретно", "саме", "точно"]):
        score += 2
    
    
    if any(word in words for word in ["по-перше", "спочатку", "потім", "нарешті"]):
        score += 2

    return score


























