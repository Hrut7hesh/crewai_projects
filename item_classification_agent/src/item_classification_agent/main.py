import os
from crewai import Agent, Crew, Task, Process, LLM

TYPE_MAPPING = {
    "Laptop": ["macbook", "thinkpad", "notebook", "ultrabook"],
    "Mobile": ["iphone", "smartphone", "android"],
    "Accessory": ["mouse", "keyboard", "charger"]
}

item_name = input("Enter item name to classify: ").strip()

classifier_agent = Agent(
    role="Item Classification Agent",
    goal="Classify items using the provided type mapping",
    backstory=(
        "You are a deterministic item classification agent.\n"
        "You MUST ONLY use the following knowledge base:\n\n"
        f"{TYPE_MAPPING}\n\n"
        "Rules:\n"
        "- Do not invent categories\n"
        "- Match keywords case-insensitively\n"
        "- If no match exists, return 'Unknown'\n"
    ),
    verbose=True
)

classification_task = Task(
    description=(
        f"Classify the item: {item_name}\n\n"
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

# This allows you to still run the file directly with 'python main.py'
if __name__ == "__main__":
    run()

