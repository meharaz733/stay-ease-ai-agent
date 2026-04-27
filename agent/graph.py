import os

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import tools_condition

from agent.nodes import agent_node, human_handover_condition, tool_node
from agent.state import AgentState, InputState, OutputState


###checkpointer---
async def get_checkpointer():
    """Return postgres saver checkpoint"""
    context_manager = AsyncPostgresSaver.from_conn_string(os.environ["DATABASE_URL"])
    checkpointer = await context_manager.__aenter__()
    await checkpointer.setup()

    return checkpointer


async def build_graph() -> CompiledStateGraph:
    """
    Construct and compile the StayEase LangGraph agent with a PostgreSQL checkpointer.

    Graph topology
    --------------
    START
      └─► agent_node                                  (LLM decides action)
            ├─► tool_node                             (if tool call requested)
            │     ├─► search_available_properties ──► agent   (results passed back to LLM)
            │     ├─► get_listing_details         ──► agent   (results passed back to LLM)
            │     ├─► create_booking              ──► agent   (results passed back to LLM)
            │     └─► human_handover              ──► END     (escalation, no further LLM call)
            └─► END                                    (if LLM replied directly)

    Returns
    -------
    CompiledStateGraph
        Compiled LangGraph application ready to invoke.
    """
    ###### GRAPH
    workflow = StateGraph(
        state_schema=AgentState,
        input_schema=InputState,
        output_schema=OutputState,
    )

    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)

    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", tools_condition)
    workflow.add_conditional_edges(
        "tools",
        human_handover_condition,
        {"end": END, "agent": "agent"},
    )

    checkpointer = await get_checkpointer()

    return workflow.compile(checkpointer=checkpointer)
