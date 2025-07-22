from ai import ai_instance
from utils import limit_text

async def make_summary(messages: list, max_tokens=256) -> str:
    if not messages:
        return "Нет новых сообщений для сводки."
    text = '\n'.join([f"{m['sender']}: {m['text']}" for m in messages])
    prompt = f"Сделай краткую сводку по этим сообщениям на русском языке:\n{text}"
    prompt = limit_text(prompt, 2048)
    summary = await ai_instance.ask(prompt, max_new_tokens=max_tokens)
    return summary.strip() 