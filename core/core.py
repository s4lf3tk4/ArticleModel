from typing import Annotated, Sequence, TypedDict, List, Literal
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class OrchestraState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    topic: str
    report_path: str
    questions: List[str]
    answer: List[str]
    phase: Literal["research", "analyze", "write"]
    iteration: int
    draft: str
