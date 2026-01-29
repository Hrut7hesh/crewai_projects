import os
from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.knowledge.source.json_knowledge_source import JSONKnowledgeSource
from .tools.jira_tool import GetUserStoriesTool

@CrewBase
class FetchCrew():
    
    jira_stories_tool = GetUserStoriesTool()
    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def fetcher(self) -> Agent:
        return Agent(
            config=self.agents_config['fetcher'],
            tools=[self.jira_stories_tool]
        )

    @task
    def fetching_task(self) -> Task:
        return Task(
            config=self.tasks_config['fetching_task']
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
        )