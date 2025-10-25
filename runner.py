
import os
from dotenv import load_dotenv
from pathlib import Path
from crewai import Crew, Process

from agents import researcher as mk_researcher, writer as mk_writer, reviewer as mk_reviewer
from tasks import research_task, writing_task, review_task
from tools.web_search import FetchUrlTool, WebSearchTool

load_dotenv()

def _format_tools_for_agent():
    return [WebSearchTool(), FetchUrlTool()]

def run_crew(topic: str) -> dict:
    """Run the Researcher->Writer->Reviewer pipeline and return artifact paths + final text."""
    outputs = Path("outputs")
    outputs.mkdir(exist_ok=True, parents=True)

    tools = _format_tools_for_agent()

    researcher = mk_researcher(tools=tools)
    writer = mk_writer()
    reviewer = mk_reviewer()

    t1 = research_task(researcher, topic)
    t2 = writing_task(writer, topic)
    t3 = review_task(reviewer)

    crew = Crew(
        agents=[researcher, writer, reviewer],
        tasks=[t1, t2, t3],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff(inputs={"topic": topic})

    artifacts = {
        "research_notes": str(outputs / "research_notes.md"),
        "draft": str(outputs / "draft.md"),
        "final": str(outputs / "final.md"),
        "result": str(result),
    }
    return artifacts
