
from crewai import Task
from pathlib import Path

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def research_task(agent, topic: str):
    return Task(
        description=(
            "Research the topic: '{topic}'.\n"
            "- Use web_search and fetch_url tools to gather 5–8 reputable sources.\n"
            "- Produce bullet points grouped by subtopic.\n"
            "- Include inline citations as [label](url).\n"
            "- Be concise and avoid speculation."
        ).format(topic=topic),
        agent=agent,
        expected_output=(
            "A concise markdown file with sections, bullet points, and citations. "
            "File path: outputs/research_notes.md"
        ),
        output_file=str(OUTPUT_DIR / "research_notes.md"),
    )

def writing_task(agent, topic: str):
    return Task(
        description=(
            "Using the research notes, write a 600–800 word article about '{topic}'.\n"
            "- Include a short intro, 2–4 headings, and a bulleted 'Key Takeaways' section.\n"
            "- Weave in citations where appropriate using [label](url)."
        ).format(topic=topic),
        agent=agent,
        expected_output=(
            "A well‑structured markdown article ready to publish. "
            "File path: outputs/draft.md"
        ),
        output_file=str(OUTPUT_DIR / "draft.md"),
    )

def review_task(agent):
    return Task(
        description=(
            "Review and improve the draft.\n"
            "- Fix inaccuracies, tighten language, ensure logical flow.\n"
            "- Ensure all claims that rely on sources have citations.\n"
            "- Output the final article."
        ),
        agent=agent,
        expected_output=(
            "Final, polished markdown. File path: outputs/final.md"
        ),
        output_file=str(OUTPUT_DIR / "final.md"),
    )
