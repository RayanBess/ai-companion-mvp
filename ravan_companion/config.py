"""Configuration and credential loading for the Ravan companion."""

from __future__ import annotations

import os

from dotenv import load_dotenv

# Load variables from a local .env file if present (no-op in production).
load_dotenv()

# The companion runs on Anthropic's most capable model by default.
MODEL = "claude-opus-4-8"

# Max tokens for a single companion reply. Generous enough for a recipe or a
# scored menu, small enough to keep latency reasonable.
MAX_TOKENS = 2048


def require_api_key() -> str:
    """Return the Anthropic API key, or raise a clear error if it's missing.

    The graph and the Streamlit app both call this so the user gets a single,
    actionable message ("add your key to .env") instead of an opaque 401.
    """
    key = _get_api_key().strip()
    if not key or key == "your-api-key-here":
        raise RuntimeError(
            "ANTHROPIC_API_KEY is not set. Locally, copy .env.example to .env "
            "and add your key. On Streamlit Cloud, add it under "
            "Settings -> Secrets. Get a key at "
            "https://console.anthropic.com/settings/keys."
        )
    return key


def _get_api_key() -> str:
    """Read the key from Streamlit secrets if available, else env vars.

    On Streamlit Cloud the key lives in the Secrets manager; locally it
    comes from a .env file. Importing streamlit is optional so the graph
    can run outside a Streamlit context (e.g. tests, CLI).
    """
    try:
        import streamlit as st

        if "ANTHROPIC_API_KEY" in st.secrets:
            return st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        pass
    return os.getenv("ANTHROPIC_API_KEY", "")
