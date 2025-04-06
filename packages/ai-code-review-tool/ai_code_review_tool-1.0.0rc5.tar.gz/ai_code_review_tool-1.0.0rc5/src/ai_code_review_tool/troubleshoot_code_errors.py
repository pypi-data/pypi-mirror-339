# src/ai_code_review_tool/troubleshoot_code_errors.py

def troubleshoot_code_errors(error_logs: str):
    """Analyze error logs or console output and suggest troubleshooting steps."""
    suggestions = []
    if "ModuleNotFoundError" in error_logs:
        suggestions.append("Check if all required modules are installed.")
    if "TypeError" in error_logs:
        suggestions.append("Check if function arguments and return types are correct.")
    if "SyntaxError" in error_logs:
        suggestions.append("Check for any missing or extra parentheses or commas.")
    
    return suggestions
