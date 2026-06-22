"""The companion's LangGraph graph.

    START → router → companion → END

`router` classifies the latest user message into an intent (see routes.py).
`companion` builds the grounded system prompt for that intent and calls Claude.
Keeping these as two nodes makes the routing explicit and easy to extend (add a
vision node, a meal-logging node, etc.) without rewriting the model call.
"""

from __future__ import annotations

from typing import Annotated, TypedDict

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

from .config import MAX_TOKENS, MODEL, require_api_key
from .prompts import build_system_prompt
from .routes import GENERAL, classify, guidance_for


class CompanionState(TypedDict):
    """State threaded through the graph."""

    messages: Annotated[list[BaseMessage], add_messages]
    intent: str


def _model() -> ChatAnthropic:
    """Instantiate the chat model, failing fast if the API key is missing."""
    require_api_key()
    return ChatAnthropic(model=MODEL, max_tokens=MAX_TOKENS, timeout=60)


def _last_user_text(messages: list[BaseMessage]) -> str:
    """Return the text of the most recent human message."""
    for message in reversed(messages):
        if isinstance(message, HumanMessage):
            content = message.content
            return content if isinstance(content, str) else str(content)
    return ""


def route_node(state: CompanionState) -> dict:
    """Classify the latest user message into an intent."""
    return {"intent": classify(_last_user_text(state["messages"]))}


def companion_node(state: CompanionState) -> dict:
    """Build the grounded prompt for the intent and call Claude."""
    system = build_system_prompt(guidance_for(state.get("intent", GENERAL)))
    response = _model().invoke([SystemMessage(content=system), *state["messages"]])
    return {"messages": [response]}


def build_graph():
    """Compile and return the companion graph."""
    graph = StateGraph(CompanionState)
    graph.add_node("router", route_node)
    graph.add_node("companion", companion_node)
    graph.add_edge(START, "router")
    graph.add_edge("router", "companion")
    graph.add_edge("companion", END)
    return graph.compile()
