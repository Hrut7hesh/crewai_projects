from item_classification.crew import ClassifyCrew

def test():
    inputs = {
        "item_name": "iPhone 15 Pro Max"
    }
    
    n_iterations = 5
    model_name = "azure/gpt-4o"
    
    try:
        ClassifyCrew().crew().test(
            n_iterations=n_iterations,
            eval_llm=model_name,
            inputs=inputs
        )
    except Exception as e:
        print(f"Error during testing: {e}")