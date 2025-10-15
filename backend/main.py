from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware # Required for the frontend to connect
from llm_service import generate_task_plan
from models import GoalInput, TaskPlan
import uvicorn
import os

# --- FastAPI Initialization ---
app = FastAPI(
    title="Smart Task Planner API",
    description="Backend for the Smart Task Planner assignment using LLM reasoning.",
    version="1.0.0"
)

# --- CORS Configuration ---
# This is crucial! It allows your frontend (running on a different port/location) 
# to make requests to this API
origins = [
    "*",  # Allow requests from any origin during development (for the HTML file)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/generate_plan", response_model=TaskPlan, summary="Break down a goal into tasks and timelines.")
async def create_plan(goal: GoalInput):
    """
    Accepts a user goal and uses the LLM to return a detailed task breakdown
    with suggested deadlines and dependencies.
    """
    try:
        # Calls the LLM service to generate the plan
        plan = generate_task_plan(goal)
        # LLM Reasoning is wrapped here
        return plan
    except EnvironmentError as e:
        # Handle API key or environment setup issues
        raise HTTPException(status_code=503, detail=f"Service Configuration Error: {e}")
    except ValueError as e:
        # Handle cases where the LLM fails to generate the required JSON structure
        raise HTTPException(status_code=500, detail=f"LLM Output Error: {e}")
    except Exception as e:
        # Catch all other unexpected errors
        raise HTTPException(status_code=500, detail=f"An unexpected server error occurred: {e}")


if __name__ == "__main__":
    # --- How to Run the Code ---
    # This command uses uvicorn to run the FastAPI app and enables auto-reload 
    # for easy development.
    # You must run this command from the 'backend/' folder.
    print("Starting FastAPI Server...")
    print("Access the API docs at: http://127.0.0.1:8000/docs")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
