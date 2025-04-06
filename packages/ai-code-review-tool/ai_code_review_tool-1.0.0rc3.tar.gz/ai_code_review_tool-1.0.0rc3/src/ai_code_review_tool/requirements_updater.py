# src/ai_code_review_tool/requirements_updater.py

import subprocess

def update_requirements():
    """
    Regenerates requirements.txt using pipreqs.
    """
    try:
        subprocess.run(["pipreqs", ".", "--force"], check=True)
        print("✅ requirements.txt updated with pipreqs.")
    except subprocess.CalledProcessError:
        print("❌ Failed to update requirements.txt. Make sure pipreqs is installed.")
