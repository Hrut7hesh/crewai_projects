import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.knowledge.source.json_knowledge_source import JSONKnowledgeSource
from typing import List

json_source = JSONKnowledgeSource(
    file_paths=["type_mapping.json"]
)

@CrewBase
class ClassifyCrew():
    
    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def classifier(self) -> Agent:
        return Agent(
            config=self.agents_config['classifier'],
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

    @task
    def classifying_task(self) -> Task:
        return Task(
            config=self.tasks_config['classifying_task']
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
        )