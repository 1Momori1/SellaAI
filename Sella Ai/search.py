try:
    from googlesearch import search
except ImportError:
    search = None
import asyncio

async def google_search(query: str, num_results: int = 5) -> list:
    if search is None:
        return ["Ошибка: googlesearch не установлен."]
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: list(search(query, num_results=num_results, lang='ru')) if search else ["Ошибка: googlesearch не установлен."]) 