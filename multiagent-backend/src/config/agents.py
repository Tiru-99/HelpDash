from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools.support_tools.tools import SUPPORT_TOOLS
from tools.dashboard_tools.tools import DASHBOARD_TOOLS

import os
from crewai import LLM

# Read your API key from the environment variable
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Use Gemini 2.5 Pro Experimental model
gemini_llm = LLM(
    model='gemini/gemini-2.5-pro',
    api_key=gemini_api_key,
    temperature=0.0  # Lower temperature for more consistent results.
)

@CrewBase
class MultiAgents():
    agents_config = "agents_config.yaml"
    tasks_config = "tasks.yaml"
    
    @agent
    def support_agent(self) -> Agent:
        agent_instance = Agent(
            config=self.agents_config["support"],
            verbose=True,
            tools=[tool() for tool in SUPPORT_TOOLS],
            llm = gemini_llm,
            memory = True
        )
        print("Support Agent created.")
        return agent_instance
    
    @agent
    def dashboard_agent(self) -> Agent:
        agent_instance = Agent(
            config=self.agents_config["dashboard"],
            verbose=True,
            tools=[tool() for tool in DASHBOARD_TOOLS],
            llm = gemini_llm
        )
        print("Dashboard Agent created.")
        return agent_instance
    
    @task
    def support_query_task(self):
        task_instance = Task(
            config=self.tasks_config["support_query_task"],
            agent=self.support_agent(),
        )
        return task_instance
    
    @task
    def dashboard_analytics_task(self):
        task_instance = Task(
            config=self.tasks_config["dashboard_analytics_task"],
            agent=self.dashboard_agent(),
        )
        return task_instance
    
    @crew
    def crew(self) -> Crew:
        crew_instance = Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
        return crew_instance
