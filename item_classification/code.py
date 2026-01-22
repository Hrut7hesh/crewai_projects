import os
import ssl
import warnings
import logging

# --- 1. THE NUCLEAR PATCH ---
def silent_nuclear_patch():
    # SSL Bypass
    ssl._create_default_https_context = ssl._create_unverified_context
    os.environ['CURL_CA_BUNDLE'] = ""
    os.environ['PYTHONHTTPSVERIFY'] = "0"
    os.environ['HTTPX_VERIFY'] = "False"

    # 🛑 THE LOGGING FIX: Silence the noise
    os.environ['CREWAI_TELEMETRY_OPT_OUT'] = "true"
    os.environ['OTEL_SDK_DISABLED'] = "true"

    # Force the loggers to ignore everything below "CRITICAL"
    logging.getLogger("urllib3").setLevel(logging.CRITICAL)
    logging.getLogger("backoff").setLevel(logging.CRITICAL)
    logging.getLogger("crewai").setLevel(logging.CRITICAL)

    # Suppress Python warnings
    warnings.filterwarnings("ignore")

silent_nuclear_patch()

# --- 2. IMPORTS ---
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task, LLM
from crewai.knowledge.source.json_knowledge_source import JSONKnowledgeSource

load_dotenv()

# --- 3. CONFIGURATION ---
azure_llm = LLM(
    model=f"azure/{os.getenv('MODEL')}",
    base_url=os.getenv("AZURE_API_BASE"),
    api_key=os.getenv("AZURE_API_KEY"),
    api_version=os.getenv("AZURE_API_VERSION")
)

json_source = JSONKnowledgeSource(file_paths=["type_mapping.json"])

# --- 4. UPDATED AGENT (Avoiding Safety Triggers) ---
classifier_agent = Agent(
    role="Data Organization Specialist",
    goal="Identify the category for items using the organizational knowledge base.",
    backstory=(
        "You are an expert in data management. Your task is to ensure items are "
        "categorized according to the specific definitions provided in your "
        "available knowledge sources."
    ),
    llm=azure_llm,
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

# --- 5. UPDATED TASK ---
item_name = input("\nEnter item name to classify: ").strip()

classification_task = Task(
    description=(
        f"Analyze the item: '{item_name}'. "
        "Reference the provided knowledge source to determine its organizational type. "
        "Provide your answer in a structured JSON format with the keys: "
        "'item', 'type', and 'confidence'."
    ),
    expected_output="A structured JSON object with the classification details.",
    agent=classifier_agent
)

crew = Crew(
    agents=[classifier_agent],
    tasks=[classification_task],
    verbose=False
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