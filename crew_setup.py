from crewai import Crew, Process
from agent import researcher_agent, writer_agent
from task import research_task, writing_task

# ── Crew Orchestration ───
crew = Crew(
    agents=[
        researcher_agent,   
        writer_agent,       
    ],
    tasks=[
        research_task,      
        writing_task,       
    ],
    process=Process.sequential,   
    verbose=True,
)
