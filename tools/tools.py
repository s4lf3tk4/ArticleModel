from langgraph.prebuilt import ToolNode
from ddgs import DDGS
import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool
from pathlib import Path
from core import WORKDIR

@tool
def web_search(query: str) -> str:
    """
    Ищет в интернете через DuckDuckGo, извлекает текст с первой найденной страницы
    и возвращает выдержку.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            if not results:
                return "Ничего не найдено."

            # Берём первую ссылку
            url = results[0]['href']
            try:
                resp = requests.get(url, timeout=10)
                soup = BeautifulSoup(resp.text, 'html.parser')
                paragraphs = soup.find_all('p')
                text = ' '.join(p.get_text() for p in paragraphs[:5])
                return f"Источник: {url}\n\n{text[:2000]}"
            except Exception as e:
                # Если не удалось извлечь, возвращаем сниппет
                return f"{results[0]['title']}: {results[0]['body']}"
    except Exception as e:
        return f"Ошибка поиска: {e}"

@tool
def save_report(content: str, path: str) -> str:
    """Сохраняет отчёт в файл."""
    try:
        full_path = WORKDIR / path
        full_path.write_text(content, encoding='utf-8')
        return f"Отчёт сохранён в {full_path}"
    except Exception as e:
        return f"Ошибка сохранения: {e}"
