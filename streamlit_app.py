
import os
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv
from runner import run_crew

load_dotenv()

st.set_page_config(page_title="CrewAI POC", page_icon="🤖", layout="wide")

st.title("🤖 CrewAI POC — Researcher · Writer · Reviewer")

with st.sidebar:
    st.header("⚙️ Settings")
    provider = st.selectbox("Model Provider", ["openai", "ollama"], index=0,
                            help="Choose OpenAI (API key required) or local Ollama")
    openai_model = st.text_input("OpenAI Model", os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    ollama_model = st.text_input("Ollama Model", os.getenv("OLLAMA_MODEL", "llama3.1:8b"))
    max_tokens = st.number_input("Max tokens", min_value=256, max_value=8192, value=int(os.getenv("MAX_TOKENS", "2000")), step=64)
    temperature = st.number_input("Temperature", min_value=0.0, max_value=2.0, value=float(os.getenv("TEMPERATURE", "0.2")), step=0.1)

    # Apply to env for CrewAI to pick up
    os.environ["MODEL_PROVIDER"] = provider
    os.environ["OPENAI_MODEL"] = openai_model
    os.environ["OLLAMA_MODEL"] = ollama_model
    os.environ["MAX_TOKENS"] = str(max_tokens)
    os.environ["TEMPERATURE"] = str(temperature)

st.markdown("""
This UI runs a three-step pipeline:

1. **Researcher** finds and summarizes sources with citations.
2. **Writer** drafts a clear article.
3. **Reviewer** tightens and finalizes the piece.
""")

topic = st.text_input("Topic", value="LLM observability best practices")

col1, col2 = st.columns([1,1])
run_button = col1.button("Run Crew", type="primary")
show_files = col2.checkbox("Show generated files", value=True)

output_box = st.empty()

def read_text(path: str) -> str:
    try:
        return Path(path).read_text(encoding="utf-8")
    except Exception as e:
        return f"⚠️ Could not read {path}: {e}"

if run_button:
    if not topic.strip():
        st.warning("Please enter a topic.")
        st.stop()

    with st.spinner("Running crew... this may take a minute"):
        artifacts = run_crew(topic.strip())

    st.success("Done!")
    final_text = read_text(artifacts["final"])
    st.subheader("✅ Final Article")
    st.markdown(final_text or "_(final.md is empty)_")

    if show_files:
        with st.expander("📄 Research Notes (research_notes.md)", expanded=False):
            st.code(read_text(artifacts["research_notes"]), language="markdown")

        with st.expander("📝 Draft (draft.md)", expanded=False):
            st.code(read_text(artifacts["draft"]), language="markdown")

st.info("Tip: Set `MODEL_PROVIDER=ollama` and pull a local model to run offline: `ollama pull llama3.1:8b`")
