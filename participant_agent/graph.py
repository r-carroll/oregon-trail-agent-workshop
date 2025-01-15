from typing import Literal, TypedDict

from dotenv import load_dotenv
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import (
    tools_condition,  # this is the checker for the if you got a tool back
)

from participant_agent.utils.nodes import (
    call_tool_model,
    is_multi_choice,
    multi_choice_structured,
    tool_node,
)
from participant_agent.utils.state import AgentState

load_dotenv()


# The graph config can be updated with LangGraph Studio which can be helpful
class GraphConfig(TypedDict):
    model_name: Literal["openai"]  # could add more LLM providers here


# TODO: define the graph to be used in testing
workflow = StateGraph(AgentState, config_schema=GraphConfig)

# Update otherwise it won't work dawg

# node 1
workflow.add_node("agent", call_tool_model)
# node 2
workflow.add_node("tools", tool_node)
workflow.add_node("multi_choice_structured", multi_choice_structured)

# entry
workflow.set_entry_point("agent")

# Conditional edge
workflow.add_conditional_edges("agent", tools_condition)
workflow.add_conditional_edges("agent",
                               is_multi_choice,
                               {"multi-choice": "multi_choice_structured", "not-multi-choice": END}
                               )

# We now add a normal edge.
workflow.add_edge("tools", "agent")
workflow.add_edge("multi_choice_structured", END)

# **graph defined here**

# Compiled graph will be picked up by workflow
graph = workflow.compile()
