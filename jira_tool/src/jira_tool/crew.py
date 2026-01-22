from jira import JIRA
from crewai import Agent, Task, Crew
from crewai.tools import tool

@tool
def getUserStories(project_key: str):
    auth = ('gelle.hrutheshreddy@gmail.com','ATATT3xFfGF0U3A7ZSvsFJEl9UxfU4it4baevQVfAHx9DuI3GeYQRI5rq4AJiqjUlTQqGPEi0AsjJ87S-j3u3aXA_vKTsBShMRSjXL10pg3EU48Obio-RhJdodjIHfRgwGhHN5MvMi6mPgLn-geQaL34Ld4ajU3FfWuhFR0SbB475jhIvupz-8E=8079240A')
    
    jira_options = {
        'server': "https://pathasuprathika77-1769072116323.atlassian.net/",
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