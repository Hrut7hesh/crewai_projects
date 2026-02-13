# from crewai.tools import BaseTool
# from typing import Type, Any
# from pydantic import BaseModel, Field
# from jira import JIRA
# import os
# import requests

# class JiraToolInput(BaseModel):
#     project_key: str = Field(..., description="The Jira project key (e.g., 'SCRUM').")

# class GetUserStoriesTool(BaseTool):
#     name: str = "get_user_stories"
#     description: str = "Fetches user stories and downloads attachments into story-specific folders only if attachments exist."
#     args_schema: Type[BaseModel] = JiraToolInput

#     async def _run(self, project_key: str) -> Any:
#         auth = (os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN"))
#         jira_options = {'server': os.getenv("JIRA_SERVER"), 'verify': False}
#         root_download_path = "output/attachments"

#         try:
#             jira = JIRA(options=jira_options, basic_auth=auth)
#             jql = f'project = "{project_key}" AND issuetype = "Story"'
#             issues = jira.search_issues(jql_str=jql, fields=['summary', 'reporter', 'assignee', 'description', 'comment', 'attachment'])

#             stories = []
#             for issue in issues:
#                 attachments_data = []
#                 story_folder = None

#                 if hasattr(issue.fields, 'attachment') and len(issue.fields.attachment) > 0:
#                     story_folder = os.path.join(root_download_path, issue.key)
#                     os.makedirs(story_folder, exist_ok=True)

#                     for attachment in issue.fields.attachment:
#                         local_filepath = os.path.join(story_folder, attachment.filename)
                        
#                         try:
#                             response = requests.get(
#                                 attachment.content, 
#                                 auth=auth, 
#                                 stream=True, 
#                                 verify=False, 
#                                 timeout=10
#                             )
#                             if response.status_code == 200:
#                                 with open(local_filepath, 'wb') as f:
#                                     for chunk in response.iter_content(chunk_size=1024):
#                                         f.write(chunk)
#                                 download_status = "Downloaded"
#                             else:
#                                 download_status = f"Failed ({response.status_code})"
#                         except Exception as err:
#                             download_status = f"Error: {str(err)}"

#                         attachments_data.append({
#                             "filename": attachment.filename,
#                             "local_path": local_filepath,
#                             "download_status": download_status
#                         })

#                 comments_data = []
#                 if hasattr(issue.fields, 'comment'):
#                     for c in issue.fields.comment.comments:
#                         comments_data.append({
#                             "author": c.author.displayName if hasattr(c, 'author') else "Unknown",
#                             "body": c.body
#                         })

#                 stories.append({
#                     "key": issue.key,
#                     "summary": issue.fields.summary,
#                     "description": issue.fields.description or "No description provided.",
#                     "reporter": issue.fields.reporter.displayName if issue.fields.reporter else "Unassigned",
#                     "assignee": issue.fields.assignee.displayName if issue.fields.assignee else "Unassigned",
#                     "comments": comments_data,
#                     "attachments": attachments_data,
#                     "has_attachments": len(attachments_data) > 0,
#                     "storage_folder": story_folder # Will be None if no attachments
#                 })

#             return stories
#         except Exception as e:
#             return f"Error: {str(e)}"

import json
from crewai.tools import BaseTool
from typing import Type, Any
from pydantic import BaseModel, Field
from jira import JIRA
import os
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class JiraTicketInput(BaseModel):
    issue_key: str = Field(..., description="The specific Jira issue key (e.g., 'SCRUM-14').")

class GetJiraTicketDetailsTool(BaseTool):
    name: str = "get_jira_ticket_details"
    description: str = "Downloads all details of a specific Jira ticket as JSON and saves its attachments in a single folder."
    args_schema: Type[BaseModel] = JiraTicketInput

    async def _run(self, issue_key: str) -> Any:
        auth = (os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN"))
        jira_options = {'server': os.getenv("JIRA_SERVER"), 'verify': False}

        try:
            jira = JIRA(options=jira_options, basic_auth=auth)
            # Fetch the issue directly
            issue = jira.issue(issue_key)
            base_path = os.path.join("output", issue_key)
            os.makedirs(base_path, exist_ok=True)
            
            # 1. Collect All Data for JSON
            ticket_data = {
                "key": issue.key,
                "summary": issue.fields.summary,
                "description": issue.fields.description,
                "status": str(issue.fields.status),
                "reporter": issue.fields.reporter.displayName if issue.fields.reporter else "None",
                "assignee": issue.fields.assignee.displayName if issue.fields.assignee else "Unassigned",
                "priority": str(issue.fields.priority),
                "created": issue.fields.created,
                "updated": issue.fields.updated,
                "components": [c.name for c in issue.fields.components],
                "comments": [
                    {"author": c.author.displayName, "body": c.body, "created": c.created}
                    for c in issue.fields.comment.comments
                ] if hasattr(issue.fields, 'comment') else []
            }

            # 2. Process and Download Attachments
            attachments_info = []
            if hasattr(issue.fields, 'attachment'):
                for attachment in issue.fields.attachment:
                    file_path = os.path.join(base_path, attachment.filename)
                    try:
                        response = requests.get(attachment.content, auth=auth, stream=True, verify=False, timeout=10)
                        if response.status_code == 200:
                            with open(file_path, 'wb') as f:
                                for chunk in response.iter_content(chunk_size=1024):
                                    f.write(chunk)
                            attachments_info.append({"filename": attachment.filename, "status": "Downloaded"})
                        else:
                            attachments_info.append({"filename": attachment.filename, "status": f"Failed ({response.status_code})"})
                    except Exception as e:
                        attachments_info.append({"filename": attachment.filename, "status": f"Error: {str(e)}"})

            ticket_data["attachments_metadata"] = attachments_info

            # 3. Save JSON file to the folder
            json_file_path = os.path.join(base_path, f"{issue_key}_details.json")
            with open(json_file_path, "w") as jf:
                json.dump(ticket_data, jf, indent=4)

            return {
                "message": f"Success. Data and attachments for {issue_key} saved to {base_path}",
                "folder_path": base_path,
                "json_file": json_file_path,
                "ticket_details": ticket_data
            }

        except Exception as e:
            return f"Error fetching ticket {issue_key}: {str(e)}"