from .prompt_mark_settings import calculate_prompt_quality

def handle_prompt_evaluation(prompt_text: str, category: str) -> int:
    return calculate_prompt_quality(prompt_text, category)