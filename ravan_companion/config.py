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
    key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not key or key == "your-api-key-here":
        raise RuntimeError(
            "ANTHROPIC_API_KEY is not set. Copy .env.example to .env and add "
            "your Anthropic API key (get one at "
            "https://console.anthropic.com/settings/keys)."
        )
    return key
