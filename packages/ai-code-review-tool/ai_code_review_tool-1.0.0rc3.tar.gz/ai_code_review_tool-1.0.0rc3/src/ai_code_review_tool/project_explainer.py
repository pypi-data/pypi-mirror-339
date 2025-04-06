# src/ai_code_review_tool/project_explainer.py

import os
import ast

def generate_how_it_works(root="src"):
    """
    Walks the project and generates a high-level overview of how the code works.
    """
    explanation = "# 🧠 How This Project Works\n\n"
    explanation += "This document is automatically generated to help you (or others) understand the structure and purpose of the project.\n\n"

    for folder, _, files in os.walk(root):
        for filename in files:
            if filename.endswith(".py"):
                path = os.path.join(folder, filename)
                rel_path = os.path.relpath(path, start=root)
                with open(path, "r", encoding="utf-8") as f:
                    try:
                        tree = ast.parse(f.read())
                    except SyntaxError:
                        continue

                explanation += f"## `{rel_path}`\n"
                explanation += f"**Path**: `{path}`\n\n"

                docstring = ast.get_docstring(tree)
                if docstring:
                    explanation += f"**Module Description**:\n> {docstring}\n\n"

                for node in tree.body:
                    if isinstance(node, ast.FunctionDef):
                        explanation += f"- `def {node.name}()` — "
                        if ast.get_docstring(node):
                            explanation += ast.get_docstring(node).split("\n")[0]
                        else:
                            explanation += "No docstring."
                        explanation += "\n"

                    elif isinstance(node, ast.ClassDef):
                        explanation += f"- `class {node.name}` — "
                        if ast.get_docstring(node):
                            explanation += ast.get_docstring(node).split("\n")[0]
                        else:
                            explanation += "No docstring."
                        explanation += "\n"
                explanation += "\n"

    return explanation
