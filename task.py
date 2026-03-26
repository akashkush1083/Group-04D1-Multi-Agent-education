from crewai import Task
from agent import researcher_agent, writer_agent

# ── Task 1 : Research ─────────
research_task = Task(
    description=(
        "Conduct thorough academic research on the topic: **{topic}**.\n\n"
        "Your research MUST cover:\n"
        "1. Clear definition and overview of the topic.\n"
        "2. Historical background or origin (if applicable).\n"
        "3. Key concepts, principles, or components.\n"
        "4. Important sub-topics a student should know.\n"
        "5. Real-world applications or examples.\n"
        "6. Common misconceptions or tricky areas for students.\n"
        "7. Suggested further reading or study resources (book titles, "
        "   websites, or course names — no made-up URLs).\n\n"
        "Present the output as a structured research brief using clear "
        "section headings so the Writer Agent can use it directly."
    ),
    expected_output=(
        "A comprehensive, structured research brief about {topic} containing: "
        "definition, background, key concepts, sub-topics, real-world examples, "
        "common misconceptions, and study resources — all clearly labelled under "
        "section headings."
    ),
    agent=researcher_agent,
)

# ── Task 2 : Writing & Formatting ───
writing_task = Task(
    description=(
        "Using the research brief provided by the Researcher Agent, create a "
        "complete, student-friendly Educational Study Guide on: **{topic}**.\n\n"
        "Your document MUST include the following sections IN ORDER:\n"
        "1. 📘 Title & Introduction  — engaging hook + what the student will learn.\n"
        "2. 🔑 Key Concepts          — concise bullet-point explanations.\n"
        "3. 📚 Detailed Explanation  — well-structured prose with sub-headings.\n"
        "4. 💡 Real-World Examples   — at least 2–3 concrete examples.\n"
        "5. ⚠️  Common Mistakes      — what students often get wrong and why.\n"
        "6. 📝 Quick-Review Summary  — 5–7 bullet takeaways.\n"
        "7. 📖 Study Resources       — books, websites, or courses to explore next.\n\n"
        "Writing guidelines:\n"
        "- Use simple, clear language suitable for a high-school or early "
        "  college student.\n"
        "- Use Markdown formatting (headings, bold, bullet points, numbered lists).\n"
        "- Keep the tone encouraging and engaging.\n"
        "- DO NOT copy-paste the research brief — synthesise and rewrite it "
        "  into polished educational prose."
    ),
    expected_output=(
        "A complete, Markdown-formatted Educational Study Guide on {topic} with "
        "all 7 required sections: Introduction, Key Concepts, Detailed Explanation, "
        "Real-World Examples, Common Mistakes, Quick-Review Summary, and Study Resources."
    ),
    agent=writer_agent,
    context=[research_task],  
)
