# src/ai_code_review_tool/generate_roadmap.py

def generate_roadmap(code_feedback: str):
    """Generate a development roadmap based on code review feedback."""
    roadmap = []
    if "refactor" in code_feedback.lower():
        roadmap.append("Refactor code for better readability and structure.")
    if "test" in code_feedback.lower():
        roadmap.append("Write unit tests to cover uncovered code paths.")
    if "feature" in code_feedback.lower():
        roadmap.append("Add new features to improve functionality.")
    if "bug" in code_feedback.lower():
        roadmap.append("Fix bugs and handle edge cases.")
    
    return roadmap
