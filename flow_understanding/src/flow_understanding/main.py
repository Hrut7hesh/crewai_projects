import json
import os
import random
from datetime import datetime
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

from flow_understanding.crews.summary_crew.summary_crew import SummaryCrew

class TopicProfile(BaseModel):
    topic: str = ""
    description: str = ""
    summary: str = ""
    status: str = "Pending"
    completion_percentage: float = 0.0

class TopicDataWorkflow(Flow[TopicProfile]):
    
    @start()
    def initialize_random_data(self):
        print("--- Step 1: Generating Random Data ---")

        topics = ["AI Integration", "Cloud Migration", "Database Optimization", "UI Redesign"]
        descriptions = [
            "User reporting latency in the dashboard.",
            "Request to upgrade the existing legacy API.",
            "System crash during high traffic peaks.",
            "New feature request for dark mode support."
        ]

        self.state.topic = random.choice(topics)
        self.state.description = random.choice(descriptions)
        
        print(f"Generated: {self.state.topic} regarding {self.state.description}")
        return "Data Initialized"

    @listen(initialize_random_data)
    def process_information(self):
        print(f"--- Step 2: Processing Data ---")

        crew_inputs = {
            "topic": self.state.topic,
            "description": self.state.description
        }
        crew_output = SummaryCrew().crew().kickoff(inputs=crew_inputs)
        self.state.summary = crew_output.raw
        
        return "Summary Created"

    @listen(process_information)
    def update_state_status(self):
        print("--- Step 3: Finalizing Status ---")
        
        self.state.status = "Processed"
        self.state.completion_percentage = 100.0
        
        return "State Finalized"

    @listen(update_state_status)
    def save_state_to_local(self):
        print("--- Step 4: Saving State to Local File ---")

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.state.topic.lower()}_{timestamp}.txt"

        state_data = self.state.model_dump()

        os.makedirs("output", exist_ok=True)
        filepath = os.path.join("output", filename)
        
        with open(filepath, "w") as f:
            json.dump(state_data, f, indent=4)
            
        print(f"Workflow data saved successfully to: {filepath}")
        return f"File saved: {filepath}"
    
def kickoff():
    workflow = TopicDataWorkflow()
    final_output = workflow.kickoff()
    
    print("\n" + "="*30)
    print(f"Final Workflow Result: {final_output}")
    print(f"Final Ticket Summary: {workflow.state.summary}")
    print("="*30)

def plot():
    """Generate a visualization of the flow"""
    flow = TopicDataWorkflow()
    flow.plot("topic_summary_flow")
    print("Flow visualization saved to topic_summary_flow.html")

if __name__ == "__main__":
    kickoff()