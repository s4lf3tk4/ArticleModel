from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
import asyncio
from graph import graph

async def main():
    app = graph.compile(checkpointer=InMemorySaver())

    init = {
        "messages": [HumanMessage(content="Первый человек в космосе")],
        "report_path": "report.md"
    }
    config = {"configurable": {"thread_id": "orchestrator-demo"}}

    result = await app.ainvoke(init, config=config)

if __name__ == "__main__":
    asyncio.run(main())
