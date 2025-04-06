# tests/test_troubleshoot_code_errors.py

import pytest
import sys
import os

# Add the src directory to sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from ai_code_review_tool.troubleshoot_code_errors import troubleshoot_code_errors

def test_troubleshoot_code_errors():
    error_logs = "ModuleNotFoundError: No module named 'requests'"
    suggestions = troubleshoot_code_errors(error_logs)
    assert "Check if all required modules are installed." in suggestions, "Expected troubleshooting suggestion."
