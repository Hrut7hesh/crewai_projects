import asyncio
from src.jira_tool.tools.jira_tool import GetUserStoriesTool

async def main():

    tool = GetUserStoriesTool()

    print("Fetching stories and downloading attachments...")
    stories = await tool._run(project_key="SCRUM")

    for story in stories:
        print(f"\n[{story['key']}] {story['summary']}")
        print(f"Reporter: {story['reporter']}")
        for att in story['attachments']:
            print(f"  - Attachment: {att['filename']} ({att['download_status']})")

if __name__ == "__main__":
    asyncio.run(main())