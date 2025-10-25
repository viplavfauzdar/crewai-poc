
from crewai import Agent
import os

def llm_model():
    provider = os.getenv("MODEL_PROVIDER", "openai").lower()
    if provider == "ollama":
        # CrewAI auto‑detects Ollama if set via env; fallback to model name
        return os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    # default: openai
    return os.getenv("OPENAI_MODEL", "gpt-4o-mini")

def researcher(tools):
    return Agent(
        role="Researcher",
        goal=(
            "Find reputable, recent sources on the given topic; extract key facts, "
            "numbers, and concise bullet points with URLs."
        ),
        backstory=(
            "You are a meticulous OSINT analyst who values verifiable sources, citation discipline, "
            "and clarity. You avoid speculation—only facts from sources you can cite."
        ),
        tools=tools,
        verbose=True,
        allow_delegation=False,
        llm=llm_model(),
    )

def writer():
    return Agent(
        role="Writer",
        goal=(
            "Write a clear, engaging, 600–800 word article that synthesizes the research "
            "into a practical narrative for senior engineers."
        ),
        backstory=(
            "You are a senior developer‑advocate and technical writer with a knack for structure, "
            "headings, and crisp takeaways."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm_model(),
    )

def reviewer():
    return Agent(
        role="Reviewer",
        goal=(
            "Critique the draft for accuracy, completeness, and flow. Tighten language, "
            "add missing context, and ensure sources are cited."
        ),
        backstory=(
            "You are a tough but fair editor. You spot logical gaps, remove fluff, and ensure "
            "the final output is precise and useful."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm_model(),
    )
