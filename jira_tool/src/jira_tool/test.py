from jira_tool.crew import FetchCrew

def test():
    inputs = {
        "project_key": "SCRUM"
    }
    
    n_iterations = 5
    model_name = "azure/gpt-4o"
    
    try:
        FetchCrew().crew().test(
            n_iterations=n_iterations,
            eval_llm=model_name,
            inputs=inputs
        )
    except Exception as e:
        print(f"Error during testing: {e}")