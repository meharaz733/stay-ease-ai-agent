from typing import Annotated, List, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class InputState(TypedDict):
    """
    Input state received from the API layer.

    This state represents the raw input from the guest.

    Fields
    ------
    messages : List of conversation messages(BaseMessage) from the guest, Agent and tools.
               This typically includes the latest user query and any prior context
               passed from the client. Messages are incrementally appended using
               the `add_messages` reducer during graph execution.
    """
    messages: Annotated[List[BaseMessage], add_messages]


class AgentState(InputState, total=False):
    """
    Internal working state shared across all nodes in the LangGraph execution.

    This state extends the InputState by including optional control flags and
    metadata used by the agent to manage flow, decision-making, and escalation.

    It evolves throughout the graph as nodes read and update fields.

    Fields
    ------
    messages : Full conversation history including user, assistant, and tool messages.
               Automatically accumulated via the `add_messages` reducer.

    is_human_needed : Boolean flag indicating whether the agent is unable to
                      confidently handle the request and requires human intervention.
                      Defaults to False if not set.

    human_handover_reason : Short explanation describing why the request is being
                            escalated to a human agent (e.g., ambiguity, unsupported
                            request, system limitation, or policy restriction).
                            Should only be set when `is_human_needed` is True.
    """

    is_human_needed: bool
    human_handover_reason: str


class OutputState(AgentState):
    """
    Final state returned to the API layer after graph execution completes.

    This state represents the resolved outcome of the agent's processing and is
    used to construct the API response.

    It typically includes:
    - The complete conversation history (including the final assistant response)
    - Any escalation signals for human handoff

    Notes
    -----
    This class currently mirrors AgentState but exists as a boundary layer.
    It allows future control over which fields are exposed externally without
    modifying the internal agent state structure.
    """
    pass
