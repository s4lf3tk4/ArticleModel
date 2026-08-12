from typing import Literal
from langchain_core.messages import HumanMessage, AIMessage
from core import MAX_SYMBOLS, MAX_ITERATIONS, OrchestraState, WORKDIR
from agents import researcher, questioner, writer

async def node_research(state: OrchestraState):
    iteration = state.get("iteration", 0) +1
    print (f"Интерация поиска информации: {iteration}")

    topic = state.get("topic", "")
    if not topic:
        for m in reversed(state["messages"]):
            if isinstance(m, HumanMessage) and m.content:
                topic = m.content
                break
    print(f"ТЕМА: {topic}")
    questions = state.get("questions")
    if questions:
        print("QUESTIONS:")
        print("--"*50)
        for q in questions:
            print(q)
        print("--"*50)
        msgs = [
            HumanMessage(content=f"Найди дополнительную информацию по следующим вопросам и ответам: {questions} по теме {state['topic']}. "
                                 f"Найди 3–5 ссылок и дай подробную информацию.")
        ]
        full_response = ""
        async for chunk in researcher.astream(
            {"messages": msgs},
            config={"configurable": {"thread_id": "research"}},
            stream_mode = "messages"
        ):
            if isinstance(chunk, AIMessage) and chunk.content and not chunk.tool_calls:
                full_response += chunk.content

        draft_old = state["draft"]
        draft_new = full_response
        combined_draft = draft_old + "\n\n" + draft_new


        return {
            "messages": [full_response],
            "topic": topic,
            "draft": combined_draft,
            "questions": [],
            "phase": "analyze",
            "iteration": iteration
        }
    else:
        print("Первичный поиск")
        msgs = [
            HumanMessage(content=f"Тема исследования: {topic}. Найди 3–5 ссылок и дай подробную информацию.")
        ]
        res = await researcher.ainvoke(
            {"messages": msgs},
            config={"configurable": {"thread_id": "research"}}
        )
        draft_new = ""
        for m in reversed(res["messages"]):
            if isinstance(m, AIMessage) and m.content:
                draft_new = m.content
                break
        return {
            "messages": res["messages"],
            "topic": topic,
            "draft": draft_new,
            "phase": "analyze",
            "iteration": iteration
        }
def router_after_research(state: OrchestraState) -> Literal["analyze", "write"]:
    return state["phase"]

async def inf_analyzer_node(state: OrchestraState):
    iteration = state.get("iteration", 0)
    if iteration >= MAX_ITERATIONS:
        print(f"Достигнут лимит итераций ({MAX_ITERATIONS}), переходим к записи.")
        return {"phase": "write"}

    draft = state.get("draft", "")
    print("DRAFT:")
    print("="*50)
    print(draft)
    print("="*50)

    if len(draft)>= MAX_SYMBOLS:
        return {"phase": "write"}

    msg = HumanMessage(content=f"Проанализируй составленный отчет:\n{draft}\n\nСоставь 1–3 точных вопроса для лучшего раскрытия темы. Верни только вопросы, каждый с новой строки.")

    full_response = ""

    async for chunk in questioner.astream(
        {"messages": [msg]},
        config={"configurable": {"thread_id": "research"}},
        stream_mode="values"
    ):
        if "messages" in chunk and chunk["messages"]:
            last_msg = chunk["messages"][-1]
            if isinstance(last_msg, AIMessage) and last_msg.content:
                full_response = last_msg.content

    questions = [q.strip() for q in full_response.split('\n') if q.strip() and '?' in q]

    if questions:
        return {"questions": questions, "phase": "research"}
    else:
        return{"phase": "write"}


def router_after_analyze(state: OrchestraState) -> Literal["research", "write"]:
    return state["phase"]

async def node_write(state: OrchestraState):

    instuction = HumanMessage(content=(
        f"Создай структурированный доклад по полученной информации {state['draft']}."
        "Верни только текст доклада в Markdown."
    ))

    full_content = ""
    async for chunk in writer.astream(
        {"messages": instuction},
        config={"configurable": {"thread_id": "write"}},
        stream_mode="values"
    ):
        if "messages" in chunk and chunk["messages"]:
            last_msg = chunk["messages"][-1]
            if isinstance(last_msg, AIMessage) and last_msg.content:
                full_content = last_msg.content
    if full_content:
        path = state["report_path"]
        full_path = WORKDIR / path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(full_content, encoding='utf-8')
        success = HumanMessage(content=f"✅ Отчёт сохранён в {full_path.absolute()}")
        print(success)
        return {"messages": [success],
                "phase": "done"
        }
    else:
        return {"messages": [HumanMessage(content="❌ Редактор не сгенерировал отчёт.")],
                "phase": "write"
        }
