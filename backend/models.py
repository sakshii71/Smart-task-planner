from pydantic import BaseModel, Field
from typing import List
from datetime import date # FastAPI/Pydantic automatically handle ISO 8601 date format for JSON

# Define the structure for a single task
class Task(BaseModel):
    task_id: int = Field(..., description="A unique integer ID for the task.")
    description: str = Field(..., description="A clear, actionable description of the task.")
    # Estimated duration in whole days
    estimated_duration_days: int = Field(..., description="The estimated time in whole days to complete the task.")
    # Date will be outputted as YYYY-MM-DD string
    suggested_deadline: date = Field(..., description="The calculated deadline for this task (YYYY-MM-DD format) based on the goal timeline and dependencies.")
    dependency_ids: List[int] = Field(default_factory=list, description="A list of task_id's that must be completed before this task can start. Use an empty list if none.")

# Define the overall output structure (The Plan)
class TaskPlan(BaseModel):
    goal: str = Field(..., description="The original goal text provided by the user.")
    # This field is crucial for the 'timeline logic' evaluation
    total_duration_days: int = Field(..., description="The LLM's estimate of the minimum number of calendar days needed to complete the goal.")
    tasks: List[Task] = Field(..., description="The detailed breakdown of tasks, timelines, and dependencies.")

# Define the input structure for the API
class GoalInput(BaseModel):
    goal_text: str = Field(..., description="The user's goal text, e.g., 'Launch a product in 2 weeks'.")
