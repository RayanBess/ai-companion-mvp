# Ravan AI Companion

A first-version prototype of the Ravan gut-microbiome AI companion: a chat
interface that turns one user's microbiome results into in-the-moment food
guidance (menu scoring, grocery lists, recipes, ingredient swaps, breakfast
ideas, and more).

- **LangGraph** orchestrates the companion: `START → router → companion → END`.
- **`langchain-anthropic`** calls Claude (`claude-opus-4-8`) under the hood.
- **Streamlit** is the chat frontend.
- The companion is grounded in a single **mocked microbiome profile**
  (`ravan_companion/profile.py`) — swap it for a real results export later.

## Project layout

```
ravan-ai-companion/
├── app.py                      # Streamlit chat UI
├── ravan_companion/
│   ├── config.py               # env loading, model + API-key handling
│   ├── profile.py              # mocked microbiome profile (the data contract)
│   ├── prompts.py              # grounded system-prompt builder
│   ├── routes.py               # intent router (menu / grocery / recipe / …)
│   └── graph.py                # the LangGraph graph
├── pyproject.toml
└── .env.example
```

## Setup

1. **Install dependencies into a local `.venv`:**

   ```sh
   uv sync
   ```

2. **Add your Anthropic API key.** Copy the example env file and paste your key:

   ```sh
   cp .env.example .env
   # then edit .env and set ANTHROPIC_API_KEY=sk-ant-...
   ```

   Get a key at <https://console.anthropic.com/settings/keys>.

3. **Run the app:**

   ```sh
   uv run streamlit run app.py
   ```

   It opens at <http://localhost:8501>. Try “Is the salmon poke bowl good for
   me?”, or use the quick-action buttons in the sidebar.

## Next steps (not in this first version)

- Image input (photograph a menu, plate, or nutrition label) via Claude vision.
- Real microbiome results instead of the mocked profile.
- Meal logging + a daily/weekly adherence summary.
- Barcode product lookup.
