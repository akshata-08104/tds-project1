import os
import requests
import subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fuzzywuzzy import fuzz
from dotenv import load_dotenv
from functions import get_task_output, extract_dayname, count_days, extract_package, get_correct_package

# Load environment variables
load_dotenv()
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")

if not AIPROXY_TOKEN:
    print("⚠️ Warning: AIPROXY_TOKEN not set. Check your .env file.")

app = FastAPI()

# Model for handling POST request JSON data
class TaskRequest(BaseModel):
    task: str

@app.get("/read")
async def read_file(path: str):
    """Reads a file from the /data directory."""
    if not path.startswith("/data"):
        raise HTTPException(status_code=400, detail="Path should start with /data")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    with open(path, "r") as file:
        content = file.read()
    return {"content": content}

@app.post("/run")
async def run_task(request: TaskRequest):
    """Executes a task based on user input."""
    try:
        task = request.task.lower()
        task_output = get_task_output(AIPROXY_TOKEN, task).lower()

        if "count" in task:
            day = extract_dayname(task)
            count_days(day)

        elif "install" in task:
            package = extract_package(task)
            correct_package = get_correct_package(package)
            if correct_package:
                subprocess.run(["pip", "install", correct_package])
                return {"status": "success", "output": f"Installed {correct_package}"}
            else:
                return {"status": "error", "output": "Package not recognized"}

        else:
            return {"status": "error", "output": "Task not supported"}

        return {"status": "success", "output": task_output}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in running task: {str(e)}")
