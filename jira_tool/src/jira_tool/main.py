from crewai import Agent, Task, Crew
from .tools.jira_tool import GetUserStoriesTool

jira_stories_tool = GetUserStoriesTool()

project_analyst = Agent(
    role="Project Analyst",
    goal="Analyze project data and generate insights from Jira",
    backstory="An experienced project analyst who uses tools to extract real-time Jira data.",
    tools=[jira_stories_tool],
    verbose=True,
    allow_delegation=False
)
project_key = input("Enter the project key to fetch the issues: ")
analysis_task = Task(
    description=(
        f"1. Use the getUserStories tool to fetch issues from project '{project_key}'.\n"
        "2. Analyze the retrieved issues.\n"
        "3. Create a summary of who is reporting the most stories and what the common themes are."
    ),
    agent=project_analyst,
    expected_output="A structured summary report of the Jira user stories found."
)

crew = Crew(
    agents=[project_analyst],
    tasks=[analysis_task]
)

def run():
    result = crew.kickoff()
    print("\nFinal Result:\n", result)

if __name__ == "__main__":
    run()