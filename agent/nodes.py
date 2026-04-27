from langchain_core.messages import SystemMessage
from langgraph.prebuilt import ToolNode

from agent.llm import llm
from agent.prompt import SYSTEM_PROMPT
from agent.state import AgentState
from agent.tools import TOOLS

model_with_tools = llm.bind_tools(TOOLS)


async def agent_node(state: AgentState) -> AgentState:
    """
    This node constructs the model input by prepending a system prompt to the
    existing conversation history, then invokes the language model (with tool
    support enabled) to produce a response.

    The generated response is appended to the state via the `messages` field,
    following the LangGraph reducer pattern (`add_messages`).

    Parameters
    ----------
    state : AgentState
        The current graph state containing the full conversation history and
        any optional control flags.

    Returns
    -------
    AgentState
        A partial state update containing:
        - messages : List[BaseMessage]
            A single-item list with the newly generated assistant message.
            This will be merged into the existing state via the reducer.
    """
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]

    response = await model_with_tools.ainvoke(messages)
    return {"messages": [response]}


tool_node = ToolNode(TOOLS)


def human_handover_condition(state: AgentState) -> str:
    """After tool_node: route to human handover or back to agent"""

    is_human_needed = state.get("is_human_needed")

    if is_human_needed:
        return "end"
    return "agent"
