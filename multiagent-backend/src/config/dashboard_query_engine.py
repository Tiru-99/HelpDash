from crewai import Crew, Task, Process
from config.agents import MultiAgents

def run_dashboard_analytics(prompt: str):
    """
    Run dashboard analytics using the MultiAgents crew
    """
    try:

        crew_instance = MultiAgents()
        
        dashboard_agent = crew_instance.dashboard_agent()
        
        #multilingual support
        multilingual_hint = "Note: Always respond in the same language as the user's query.\n\n"
        final_prompt = multilingual_hint + prompt
        
        custom_task = Task(
            description=final_prompt,
            agent=dashboard_agent,
            expected_output="Detailed analytics report with metrics and insights"
        )
        
        crew = Crew(
            agents=[dashboard_agent],
            tasks=[custom_task],
            process=Process.sequential,
            verbose=True,
            memory = True , 
            embedder={
                "provider": "huggingface",
                "config": {
                    "model": "all-MiniLM-L6-v2"
                }
            }
        )
        
        result = crew.kickoff()
        
        # Try to extract the actual content
        if result:
            if hasattr(result, 'raw'):
                actual_result = result.raw
                print(f"[INFO] Extracted raw content: {actual_result}")
            elif hasattr(result, 'result'):
                actual_result = result.result
                print(f"[INFO] Extracted result content: {actual_result}")
            elif hasattr(result, 'output'):
                actual_result = result.output
                print(f"[INFO] Extracted output content: {actual_result}")
            else:
                actual_result = str(result)
                print(f"[INFO] Converted to string: {actual_result}")
                
            print("[INFO] Crew execution complete.")
            return actual_result
        else:
            print("[WARNING] Result is None or empty")
            return "No analytics generated"
        
    except Exception as e:
        print(f"[ERROR] Error running dashboard analytics: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"Error: {str(e)}"
