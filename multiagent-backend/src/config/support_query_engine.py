
from crewai import Crew, Task, Process
from config.agents import MultiAgents

def run_support_query(prompt: str):
    """
    Run a support query using the MultiAgents crew
    """
    try:

        crew_instance = MultiAgents()
        
        support_agent = crew_instance.support_agent()
        
        #multilingual prompt support 
        custom_task = Task(
            description=f"User Query: {prompt}\n\nPlease provide a comprehensive response to this user query. Use available tools if needed and provide a clear, helpful answer. Note: Always respond in the same language as the user's query.\n\n",
            agent=support_agent,
            expected_output="A clear, comprehensive response to the user's query with specific details and actionable information."
        )
        
        crew = Crew(
            agents=[support_agent],
            tasks=[custom_task],
            process=Process.sequential,
            verbose=True,
            memory = True,
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
            # If result is a CrewOutput object, get the raw content
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
            return "No response generated"
        
    except Exception as e:
        print(f"[ERROR] Error running support query: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"Error: {str(e)}"
