import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

from crewai import Agent

# ── Researcher Agent ────────

llm=ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    max_tokens=400
)
researcher_agent = Agent(
    role="Education Researcher",
    goal=(
        "Source comprehensive, accurate study resources and factual information "
        "about {topic}. Gather definitions, key concepts, important sub-topics, "
        "real-world examples, and reputable references that a student would need."
    ),
    backstory=(
        "You are a seasoned academic researcher with expertise across multiple "
        "disciplines. You have spent years curating study materials for universities "
        "and e-learning platforms. You know exactly what a student needs to build a "
        "solid understanding of any topic — from foundational definitions to advanced "
        "nuances. You hand off a rich, well-organised research brief to the Writer "
        "so they can craft the perfect learning document."
    ),
    llm="groq/llama-3.1-8b-instant",
    verbose=True,
    allow_delegation=False,   
)

# ── Writer Agent ─────────
writer_agent = Agent(
    role="Education Content Writer",
    goal=(
        "Synthesise the research findings about {topic} into a well-structured, "
        "engaging educational document. Format it with clear headings, bullet "
        "points, examples, and a summary so any student can learn effectively."
    ),
    backstory=(
        "You are an award-winning educational content writer who has authored "
        "textbooks, online courses, and explainer guides used by millions of "
        "students worldwide. You excel at taking dense research and transforming "
        "it into clear, logically sequenced, and visually well-structured content. "
        "You always write with the student in mind — simple language, vivid "
        "examples, and a friendly yet authoritative tone."
    ),
    llm="groq/llama-3.1-8b-instant",
    verbose=True,
    allow_delegation=False,  
)
