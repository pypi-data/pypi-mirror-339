import os
from src.ai_code_review_tool.walk_project import walk_project
from src.ai_code_review_tool.chunk_file import chunk_file
from src.ai_code_review_tool.get_code_review_suggestions import get_code_review_suggestions
from src.ai_code_review_tool.generate_roadmap import generate_roadmap


async def walk_and_review_project(project_root="."):
    """Walk the project directory, review the code, and generate a roadmap."""
    files_to_review = walk_project(root_dir=project_root)
    print(f"Files to review: {files_to_review}")

    if not files_to_review:
        return [], []

    os.makedirs("reviews", exist_ok=True)
    all_feedbacks = []

    for file in files_to_review:
        print(f"Reviewing file: {file}")
        chunks = chunk_file(file)

        file_feedback = []
        for chunk in chunks:
            feedback = await get_code_review_suggestions(chunk, "Frontend")
            if feedback:
                file_feedback.append(feedback)
                all_feedbacks.append(feedback)

        # Save feedback per file
        output_filename = file.replace("/", "_").replace("\\", "_")
        output_path = f"reviews/{output_filename}.md"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# Code Review for `{file}`\n\n")
            f.write("\n\n---\n\n".join(file_feedback))

    # Step 3: Generate roadmap
    roadmap = []
    for feedback in all_feedbacks:
        roadmap.extend(generate_roadmap(feedback))

    # Save roadmap
    with open("reviews/_ROADMAP.md", "w", encoding="utf-8") as f:
        f.write("# Project Code Review Roadmap\n\n")
        for item in roadmap:
            f.write(f"- {item}\n")

    print("Code review complete. See `reviews/` folder for results.")
    return all_feedbacks, roadmap

if __name__ == "__main__":
    import asyncio
    asyncio.run(walk_and_review_project(project_root="src"))