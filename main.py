"""
Multi-Agent Education System
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Entry point for the system.

Workflow
--------
1. User enters an educational topic.
2. Researcher Agent sources key concepts, facts, and study resources.
3. Writer Agent synthesises the research into a structured Study Guide.
4. The final guide is printed to the terminal AND saved as a .md file.

Run
---
    python main.py
"""

import os
import re
from datetime import datetime
from crew_setup import crew


# ── Helpers ────────

def safe_filename(topic: str) -> str:
    """Convert a topic string into a filesystem-safe filename."""
    slug = re.sub(r"[^\w\s-]", "", topic.lower())
    slug = re.sub(r"[\s]+", "_", slug).strip("_")
    return slug[:60]  # cap length


def save_guide(topic: str, content: str) -> str:
    """Save the study guide to a Markdown file and return the path."""
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{safe_filename(topic)}_{timestamp}.md"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# Educational Study Guide: {topic}\n")
        f.write(f"*Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')}*\n\n")
        f.write("---\n\n")
        f.write(str(content))

    return filepath


def print_banner():
    print("\n" + "═" * 60)
    print("   🎓  Multi-Agent Education System")
    print("   Powered by CrewAI + Groq (LLaMA 3.1)")
    print("═" * 60)
    print("   Agents  : Researcher  →  Writer")
    print("   Output  : Structured Educational Study Guide")
    print("═" * 60 + "\n")


# ── Main

def main():
    print_banner()

    topic = input("📚 Enter an educational topic: ").strip()
    if not topic:
        print("❌ No topic entered. Please re-run and provide a topic.")
        return

    print(f"\n🔍 Researcher Agent  → sourcing study resources for: '{topic}'")
    print("✍️  Writer Agent      → will synthesise into a study guide")
    print("⏳ Running the crew (this may take a moment)...\n")
    print("─" * 60)

    result = crew.kickoff(inputs={"topic": topic})

    print("\n" + "═" * 60)
    print("   ✅  FINAL EDUCATIONAL STUDY GUIDE")
    print("═" * 60 + "\n")
    print(result)

    filepath = save_guide(topic, result)
    print("\n" + "─" * 60)
    print(f"💾 Study guide saved to: {filepath}")
    print("─" * 60 + "\n")


if __name__ == "__main__":
    main()
