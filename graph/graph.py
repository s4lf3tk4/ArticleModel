from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from core import OrchestraState
from nodes import node_research, inf_analyzer_node, node_write

graph = StateGraph(OrchestraState)
graph.add_node("research", node_research)
graph.add_node("analyze", inf_analyzer_node)
graph.add_node("write", node_write)

graph.set_entry_point("research")
graph.add_conditional_edges("research", lambda s: s["phase"], {"analyze": "analyze", "write": "write"})
graph.add_conditional_edges("analyze", lambda s: s["phase"], {"research": "research", "write": "write"})
