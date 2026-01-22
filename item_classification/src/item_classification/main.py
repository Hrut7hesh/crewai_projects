import os

from crewai import Agent, Crew, Task, Process
from crewai.knowledge.source.json_knowledge_source import JSONKnowledgeSource

json_source = JSONKnowledgeSource(
    file_paths=["type_mapping.json"]
)

classifier_agent = Agent(
    role='Intelligent Item Classifier',
    goal='Map items to categories based on the knowledge base, using technical context when necessary.',
    backstory=(
        "You are an expert taxonomist with deep knowledge of technology and consumer goods. "
        "While you must stick to the categories defined in the knowledge base, you are "
        "expected to use your internal knowledge to identify synonyms and relationships. "
        "For example, if an item is 'iOS', you recognize it belongs to the 'Phone' or 'Mobile' category "
        "if those exist in your mapping."
    ),
    knowledge_sources=[json_source],
    embedder={
        "provider": "azure",
        "config": {
          "deployment_id": os.getenv("AZURE_EMBEDDING_DEPLOYMENT_NAME"),
          "api_key": os.getenv("AZURE_API_KEY"),
          "api_base": os.getenv("AZURE_API_BASE"),
          "api_version": os.getenv("AZURE_API_VERSION"),
          }
    }
)

item_name = input("Enter item name to classify: ").strip()

classification_task = Task(
    description=(
        f"Classify the following item: '{item_name}'\n\n"
        "Instructions:\n"
        "1. Compare the item to the provided type mapping.\n"
        "2. If the item is a specific brand, OS, or component (e.g., 'iOS', 'Android', 'Snapdragon'), "
        "map it to its parent category (e.g., 'Phone') found in the mapping.\n"
        "- Match keywords case-insensitively.\n"
        "- If no logical match or parent category exists, return 'Unknown'.\n\n"
        "Return STRICT JSON only:\n"
        "{\n"
        "  \"item_name\": string,\n"
        "  \"item_type\": string,\n"
        "  \"matched_keyword\": string | null,\n"
        "  \"confidence\": \"High\" | \"Medium\" | \"Low\"\n"
        "}"
    ),
    agent=classifier_agent,
    expected_output="JSON classification result"
)

crew = Crew(
    agents=[classifier_agent],
    tasks=[classification_task],
    process=Process.sequential,
    verbose=True
)

def run():
    """
    This function is what 'uv run run_crew' looks for.
    """
    result = crew.kickoff()
    print("\nFinal Result:\n", result)

if __name__ == "__main__":
    run()