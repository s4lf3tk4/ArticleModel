from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from tools import web_search, save_report

def create_questioner():
    model = ChatOllama(model="llama3.2:3b", base_url="http://localhost:11434", num_predict=2000)
    sys = SystemMessage(content=(
        "Ты – помощник по сбору информации. Проанализируй предоставленную сводку и определи, "
        "каких данных не хватает для полноценного отчёта. Сформулируй вопрос или вопросы, которые помогут "
        "получить недостающую информацию. Верни вопросы списком."
    ))
    tools = []
    return create_react_agent(
        model=model,
        tools=tools,
        prompt=sys,
        checkpointer=InMemorySaver()
    )

def create_researcher():
    model = ChatOllama(model="llama3.2:3b", base_url="http://localhost:11434", num_predict=2000)
    sys = SystemMessage(content=(
        "Ты Исследователь. Твоя задача: найти 3–5 релевантных ссылок, "
        "полностью отразить их содержимое."
        "Всегда используй инструмент web_search."
        "ЗАПРЕЩЕНО ВОЗВРАЩАТЬ ССЫЛКИ НА ИСТОЧНИКИ"
        "ТВОЯ ЗАДАЧА - ПОИСК"
    ))
    tools = [web_search]
    return create_react_agent(
        model=model,
        tools=tools,
        prompt=sys,
        checkpointer=InMemorySaver()
    )

def create_writer():
    model = ChatOllama(model="llama3.2:3b", base_url="http://localhost:11434", num_predict=2000)
    sys = SystemMessage(content=(
        "Ты Писарь. Получив данные (сводку), создай читабельный отчёт в txt. "
        "Сохрани результат на диск через save_report и верни краткое резюме."
    ))
    tools = [save_report]
    return create_react_agent(
        model=model,
        tools=tools,
        prompt=sys,
        checkpointer=InMemorySaver()
    )

# Создаём экземпляры агентов один раз
questioner = create_questioner()
researcher = create_researcher()
writer = create_writer()
