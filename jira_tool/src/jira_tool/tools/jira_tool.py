from crewai.tools import BaseTool
from typing import Type, Any
from pydantic import BaseModel, Field
from jira import JIRA
import os

class JiraToolInput(BaseModel):
    project_key: str = Field(..., description="The Jira project key (e.g., 'SCRUM').")

class GetUserStoriesTool(BaseTool):
    name: str = "get_user_stories"
    description: str = "Fetches user stories from a specific Jira project key."
    args_schema: Type[BaseModel] = JiraToolInput

    def _run(self, project_key: str) -> Any:
        auth =( os.getenv("JIRA_EMAIL"),
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