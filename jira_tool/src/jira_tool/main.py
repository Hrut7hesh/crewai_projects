# from crewai import Agent, Task, Crew
# from .tools.jira_tool import GetUserStoriesTool

# jira_stories_tool = GetUserStoriesTool()

# project_analyst = Agent(
#     role="Project Analyst",
#     goal="Analyze project data and generate insights from Jira",
#     backstory="An experienced project analyst who uses tools to extract real-time Jira data.",
#     tools=[jira_stories_tool],
# )
# project_key = input("Enter the project key to fetch the issues: ")
# analysis_task = Task(
#     description=(
#         f"1. Use the getUserStories tool to fetch issues from project '{project_key}'.\n"
#         "2. Analyze the retrieved issues.\n"
#         "3. Create a summary of who is reporting the most stories and what the common themes are."
#     ),
#     agent=project_analyst,
#     expected_output="A structured summary report of the Jira user stories found."
# )

# crew = Crew(
#     agents=[project_analyst],
#     tasks=[analysis_task]
# )

# def run():
#     result = crew.kickoff()
#     print("\nFinal Result:\n", result)

# if __name__ == "__main__":
#     run()

# import os
# import json
# from .crew import FetchCrew

# def run():
#     inputs = {
#         'project_key': 'SCRUM'
#     }

#     result = FetchCrew().crew().kickoff(inputs=inputs)

#     print("\n\n=== FINAL REPORT ===\n\n")
#     print(result.raw)

#     output_dir = "output"
#     os.makedirs(output_dir, exist_ok=True)

#     file_path = os.path.join(output_dir, "jira_stories.json")

#     try:
#         if result.json_dict:
#             data_to_save = result.json_dict
#         else:
#             try:
#                 data_to_save = json.loads(result.raw)
#             except json.JSONDecodeError:
#                 data_to_save = {"report": result.raw}

#         with open(file_path, "w", encoding="utf-8") as f:
#             json.dump(data_to_save, f, indent=4)
        
#         print(f"\n[SUCCESS] Report saved to {file_path}")

#     except Exception as e:
#         print(f"\n[ERROR] Failed to save JSON: {e}")

# if __name__ == "__main__":
#     run()

# import asyncio
# from .tools.jira_tool import GetUserStoriesTool

# async def run_tool_logic():
#     tool = GetUserStoriesTool()
#     print("Fetching stories and downloading attachments...")
    
#     stories = await tool._run(project_key="SCRUM")

#     if not stories:
#         print("No stories found for this project key.")
#         return

#     if isinstance(stories, str) and "Error" in stories:
#         print(f"Jira Error: {stories}")
#         return

#     print(f"--- Found {len(stories)} Stories ---")
#     for story in stories:
#       print(f"\n{'='*50}")
#       print(f"TICKET: [{story['key']}] {story['summary']}")
#       print(f"{'='*50}")
#       print(f"Assignee:  {story['assignee']}")
#       print(f"Reporter:  {story['reporter']}")
#       print(f"\nDescription:\n{story['description']}")
#       print(f"\nComments ({len(story['comments'])}):")
#       if story['comments']:
#           for comment in story['comments']:
#               print(f"  - {comment['author']}: {comment['body']}")
#       else:
#           print("  - No comments available.")

#       print(f"\nAttachments:")
#       if story.get('attachments'):
#           for att in story['attachments']:
#               status = att.get('status') or att.get('download_status', 'Unknown')
#               print(f"  - {att['filename']} ({status})")
#               print(f"    Path: {att['local_path']}")
#       else:
#           print("  - No attachments found.")
      
#       print(f"{'='*50}\n")

# def run():
#     """
#     This is the entry point CrewAI looks for. 
#     It bridges the synchronous execution to your async tool logic.
#     """
#     try:
#         asyncio.run(run_tool_logic())
#     except KeyboardInterrupt:
#         print("Execution cancelled.")

# if __name__ == "__main__":
#     run()

import asyncio
from .tools.jira_tool import GetJiraTicketDetailsTool

async def run_tool_logic():
    tool = GetJiraTicketDetailsTool()
    print("Fetching stories and downloading attachments...")
    
    story = await tool._run(issue_key="SCRUM-15")

    if not story:
        print("No stories found for this project key.")
        return

    if isinstance(story, str) and "Error" in story:
        print(f"Jira Error: {story}")
        return
    print(f"\n{'='*50}")
    print(f"TICKET: [{story['ticket_details']['key']}] {story['ticket_details']['summary']}")
    print(f"{'='*50}")
    print(f"Assignee:  {story['ticket_details']['assignee']}")
    print(f"Reporter:  {story['ticket_details']['reporter']}")
    print(f"\nDescription:\n{story['ticket_details']['description']}")
    print(f"\nComments ({len(story['ticket_details']['comments'])}):")
    if story['ticket_details']['comments']:
        for comment in story['ticket_details']['comments']:
            print(f"  - {comment['author']}: {comment['body']}")
    else:
        print("  - No comments available.")

    print(f"\nAttachments:")
    attachments = story["ticket_details"].get("attachments_metadata", [])
    
    if attachments:
        for att in attachments:
            print(f"  - {att.get('filename')} ({att.get('status')})")
    else:
        print("  - No attachments found.")
    
    print(f"{'='*50}\n")

def run():
    """
    This is the entry point CrewAI looks for. 
    It bridges the synchronous execution to your async tool logic.
    """
    try:
        asyncio.run(run_tool_logic())
    except KeyboardInterrupt:
        print("Execution cancelled.")

if __name__ == "__main__":
    run()