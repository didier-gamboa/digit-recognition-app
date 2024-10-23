import subprocess
import os

if __name__ == "__main__":
    # Backend and Frontend Initialization
    backend_process = subprocess.Popen(["uvicorn", "backend.main:app", "--reload"])
    streamlit_process = subprocess.Popen(["streamlit", "run", "./frontend/app.py"])

    backend_process.wait()
    streamlit_process.wait()