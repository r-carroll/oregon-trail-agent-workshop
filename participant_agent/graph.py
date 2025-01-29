from typing import Literal, TypedDict

from dotenv import load_dotenv
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import (
    tools_condition,  # this is the checker for the if you got a tool back
)

from participant_agent.utils.nodes import call_tool_model, structure_response, tool_node
from participant_agent.utils.state import AgentState

load_dotenv()


# Define the config
class GraphConfig(TypedDict):
    model_name: Literal["openai", "ollama"]


<<<<<<< HEAD
# Define the function that determines whether to continue or not
def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    # If there is no function call, then we respond to the user
    if not last_message.tool_calls:
        return "structure_response"
    # Otherwise if there is, we continue
    else:
        return "continue"


# TODO: define the graph to be used in testing
# workflow = StateGraph(AgentState, config_schema=GraphConfig)
=======
# Define a new graph
workflow = StateGraph(AgentState, config_schema=GraphConfig)
>>>>>>> 1a4544d (clear 3 modules)

# Define the two nodes we will cycle between
workflow.add_node("agent", call_tool_model)
# workflow.add_node("respond", respond)
workflow.add_node("tools", tool_node)
workflow.add_node("multi_choice_structured", multi_choice_structured)

# Set the entrypoint as `agent`
# This means that this node is the first one called
workflow.set_entry_point("agent")

# We now add a conditional edge
workflow.add_conditional_edges(
    "agent",
    tools_condition,
)

workflow.add_conditional_edges(
    "agent",
    is_multi_choice,
    {"multi-choice": "multi_choice_structured", "not-multi-choice": END},
)

# We now add a normal edge from `tools` to `agent`.
# This means that after `tools` is called, `agent` node is called next.
workflow.add_edge("tools", "agent")
workflow.add_edge("multi_choice_structured", END)


# Finally, we compile it!
# This compiles it into a LangChain Runnable,
# meaning you can use it as you would any other runnable
graph = workflow.compile()
