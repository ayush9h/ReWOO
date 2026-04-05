from langgraph.graph import END, START, StateGraph

from ag_workflows.executor_workflow import executor_node
from ag_workflows.planner_workflow import planner_node
from schemas.agent_schema import AgentState

graph = StateGraph(AgentState)
graph.add_node("planner", planner_node)
graph.add_node("executor", executor_node)

graph.add_edge(START, "planner")
graph.add_edge("planner", "executor")
graph.add_edge("executor", END)


app = graph.compile()
