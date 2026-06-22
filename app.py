"""Streamlit chat frontend for the Ravan AI companion.

Run with:  uv run streamlit run app.py
"""

from __future__ import annotations

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from ravan_companion.config import require_api_key
from ravan_companion.graph import build_graph
from ravan_companion.profile import avoid, recommended, summary

st.set_page_config(page_title="Ravan AI Companion", page_icon="🦠")
st.title("🦠 Ravan — Gut Microbiome Companion")

# Fail fast with a friendly message if the API key isn't configured.
try:
    require_api_key()
except RuntimeError as error:
    st.error(str(error))
    st.stop()


@st.cache_resource
def get_graph():
    """Compile the graph once per server process."""
    return build_graph()


graph = get_graph()

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar: profile snapshot + quick actions ---------------------------------
with st.sidebar:
    st.header("Your profile")
    st.caption(summary())

    def _names(items: list) -> str:
        return ", ".join(s["name"] for s in items)

    st.markdown("**Top to favour:** " + _names(recommended(8)))
    st.markdown("**Top to limit:** " + _names(avoid(8)))

    st.divider()
    st.header("Quick actions")
    quick = None
    if st.button("🍳 Breakfast idea", use_container_width=True):
        quick = "Give me a breakfast idea for this morning."
    if st.button("🛒 Grocery list", use_container_width=True):
        quick = "Generate a grocery list optimised for my microbiome."
    if st.button("🍲 Recipe for dinner", use_container_width=True):
        quick = "Suggest a dinner recipe that's good for my gut."
    if st.button("🧹 Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- Render conversation so far ------------------------------------------------
for message in st.session_state.messages:
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(message.content)

# --- Handle new input (chat box or a quick-action button) ----------------------
prompt = st.chat_input("Ask about a food, menu, recipe…") or quick

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    history = st.session_state.messages + [HumanMessage(content=prompt)]
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            result = graph.invoke({"messages": history})
        reply = result["messages"][-1]
        st.markdown(reply.content)

    # Persist the full updated history for the next turn.
    st.session_state.messages = result["messages"]
