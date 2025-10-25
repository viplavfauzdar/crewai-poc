
import os
from dotenv import load_dotenv
from pathlib import Path
import typer
from rich import print
from crewai import Crew, Process

from agents import researcher as mk_researcher, writer as mk_writer, reviewer as mk_reviewer
from tasks import research_task, writing_task, review_task
from tools.web_search import FetchUrlTool, WebSearchTool

load_dotenv()

app = typer.Typer(add_completion=False)

def format_tools_for_agent():
    return [WebSearchTool(), FetchUrlTool()]

@app.command()
def run(topic: str = typer.Option(..., "--topic", "-t", help="Topic to research and write about")):
    outputs = Path("outputs")
    outputs.mkdir(exist_ok=True, parents=True)

    tools = format_tools_for_agent()

    researcher = mk_researcher(tools=tools)
    writer = mk_writer()
    reviewer = mk_reviewer()

    t1 = research_task(researcher, topic)
    t2 = writing_task(writer, topic)
    t3 = review_task(reviewer)

    crew = Crew(
        agents=[researcher, writer, reviewer],
        tasks=[t1, t2, t3],
        process=Process.sequential,  # Research -> Write -> Review
        verbose=True,
    )

    print(f"[bold green]Starting Crew for topic:[/bold green] {topic}")
    result = crew.kickoff(inputs={"topic": topic})
    print("\n[bold cyan]Final output saved to:[/bold cyan] outputs/final.md")
    print("\n" + str(result))

if __name__ == "__main__":
    app()
