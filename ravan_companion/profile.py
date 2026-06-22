"""Mocked microbiome profile for one demo user.

This single JSON object is the contract the whole companion consumes — it is
injected into the system prompt so every reply is grounded in *this* user's
results instead of generic nutrition advice. Swap it out for a real results +
modifiers export when the modelling pipeline is wired in.
"""

from __future__ import annotations

PROFILE: dict = {
    "user": "demo",
    "display_name": "Sample User",
    "summary": (
        "Low microbial diversity; low short-chain-fatty-acid producers; "
        "mild inflammatory markers."
    ),
    "key_taxa": {
        "low": [
            "Faecalibacterium prausnitzii",
            "Akkermansia muciniphila",
            "Roseburia",
        ],
        "high": ["Bilophila wadsworthia"],
    },
    "modifiers": {
        "increase": [
            "soluble fibre",
            "polyphenols",
            "fermented foods",
            "omega-3",
            "resistant starch",
        ],
        "reduce": [
            "red & processed meat",
            "added sugar",
            "ultra-processed foods",
            "saturated fat",
            "alcohol",
        ],
    },
    "goals": ["improve diversity", "reduce bloating"],
    "restrictions": ["no shellfish"],
}
