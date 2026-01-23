from jira import JIRA
from crewai import Agent, Task, Crew
from crewai.tools import tool
import os

@tool
def getUserStories(project_key: str):
    auth = ( os.getenv("JIRA_EMAIL"),
            os.getenv("JIRA_API_TOKEN"))
    
    jira_options = {
        'server': os.getenv("JIRA_SERVER"),
        'verify': False
    }

    try:
        jira = JIRA(options=jira_options, basic_auth=auth)
        jql = f'project = "{project_key}" AND issuetype = "Story"'
        issues = jira.search_issues(jql_str=jql)

        stories = []
        for issue in issues:
            stories.append({
                "key": issue.key,
                "summary": issue.fields.summary,
                "reporter": issue.fields.reporter.displayName if issue.fields.reporter else "Unassigned"
            })
        return stories
    except Exception as e:
        return f"Error connecting to Jira: {str(e)}"

project_analyst = Agent(
    role="Project Analyst",
    goal="Analyze project data and generate insights from Jira",
    backstory="An experienced project analyst who uses tools to extract real-time Jira data.",
    tools=[getUserStories],
    verbose=True,
    allow_delegation=False
)

analysis_task = Task(
    description=(
        "1. Use the getUserStories tool to fetch issues from project 'SCRUM'.\n"
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