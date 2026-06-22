"""Intent routing for the companion.

The graph's router node classifies each incoming message into one of these
intents using cheap keyword heuristics (no extra LLM call), then the companion
node folds the matching guidance into the system prompt. This keeps every
feature from the user stories — menu scoring, grocery lists, recipes,
substitutions, plate checks, breakfast picks — behind one model call.

Swap `classify` for an LLM classifier later if keyword matching proves too
blunt; the rest of the graph doesn't change.
"""

from __future__ import annotations

GENERAL = "general"

# intent -> (keywords that trigger it, extra system-prompt guidance)
_ROUTES: dict[str, tuple[tuple[str, ...], str]] = {
    "menu": (
        ("menu", "order", "restaurant", "eating out", "dish on the"),
        "The user is choosing from a menu. If they list or photograph dishes, "
        "score each one (👍 / 😐 / 👎) and finish by naming the single best "
        "choice for their microbiome.",
    ),
    "grocery": (
        ("grocery", "groceries", "shopping list", "shop", "supermarket", "buy"),
        "The user wants a shopping list. Produce a categorised list (produce, "
        "pantry, fridge, etc.) of foods that lean on their recommended modifiers "
        "and steer clear of the ones to limit or avoid.",
    ),
    "recipe": (
        ("recipe", "cook", "make for dinner", "how do i make", "meal"),
        "The user wants to cook. Give a complete recipe — ingredients with "
        "quantities, then numbered steps — biased toward their recommended "
        "modifiers and away from the ones to limit or avoid.",
    ),
    "substitution": (
        ("substitute", "swap", "replace", "instead of", "don't like", "alternative"),
        "The user wants ingredient swaps. Suggest near-equivalent replacements "
        "that keep the dish working while improving it for their microbiome.",
    ),
    "plate": (
        ("on my plate", "about to eat", "this meal", "is this good", "in front of me"),
        "The user is about to eat a specific meal. Give a quick verdict and, if "
        "it's not ideal, one easy tweak to make it more microbiome-friendly.",
    ),
    "breakfast": (
        ("breakfast", "morning", "start my day", "wake up"),
        "The user wants a breakfast idea. Suggest one concrete, easy-to-make "
        "breakfast tuned to their profile, with a one-line reason.",
    ),
}


def classify(text: str) -> str:
    """Return the best-matching intent for a user message."""
    lowered = (text or "").lower()
    for intent, (keywords, _guidance) in _ROUTES.items():
        if any(kw in lowered for kw in keywords):
            return intent
    return GENERAL


def guidance_for(intent: str) -> str:
    """Return the system-prompt guidance snippet for an intent (or '')."""
    if intent in _ROUTES:
        return "\nFor this request: " + _ROUTES[intent][1]
    return ""
