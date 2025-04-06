# src/ai_code_review_tool/chunk_file.py

def chunk_file(file_path, chunk_size=500):
    """Chunks a file into smaller parts if it's too large to process at once."""
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    chunks = []
    for i in range(0, len(lines), chunk_size):
        chunk = "".join(lines[i:i+chunk_size])
        chunks.append(chunk)
    
    return chunks
