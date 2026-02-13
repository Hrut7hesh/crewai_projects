from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class SummaryCrew():
    """Crew for generating technical summaries"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def summary_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['summary_specialist'],
            verbose=True
        )

    @task
    def generate_summary_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_summary_task'],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )