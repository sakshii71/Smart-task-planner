import os
import json
from datetime import date, timedelta
from google import genai
from google.genai.types import GenerateContentConfig
from models import TaskPlan, GoalInput

# --- LLM Usage Guidance: Prompt Example: "Break down this goal..." ---
# This System Instruction addresses Task Completeness, Timeline Logic, and LLM Reasoning
SYSTEM_INSTRUCTION = """
You are an expert Project Manager AI. Your job is to break down the user's high-level goal into a series of detailed, actionable tasks.

CRITICAL INSTRUCTIONS:
1.  **Strict JSON Output**: You MUST respond ONLY with a single JSON object that strictly adheres to the provided TaskPlan schema. Do not include any conversational text, explanations, or markdown outside the JSON block.
2.  **Tasks**: Create a logical, sequential list of tasks (5 to 10 tasks minimum for a complex goal).
3.  **Timeline Logic**: The estimated_duration_days must logically result in the suggested_deadline, considering dependencies and the CURRENT_DATE.
4.  **Dependencies**: Define task dependencies using task IDs (e.g., Task 3 depends on Task 2). Task 1 usually has no dependencies.
5.  **Date Calculation**: Use the CURRENT_DATE as the starting point. All suggested_deadlines must be in YYYY-MM-DD format.

CURRENT DATE (Today): {current_date}
GOAL TEXT: {goal_text}
"""

def generate_task_plan(goal_input: GoalInput) -> TaskPlan:
    """Communicates with the LLM to generate a structured task plan."""
    
    # 1. Initialization: Client automatically picks up GEMINI_API_KEY from environment
    try:
        client = genai.Client()
    except Exception as e:
        # Check if the API key is missing or invalid
        raise EnvironmentError(f"Gemini client failed. Is GEMINI_API_KEY set? Error: {e}")

    current_date = date.today().isoformat()
    
    # 2. Build the LLM Prompt
    prompt = SYSTEM_INSTRUCTION.format(
        current_date=current_date,
        goal_text=goal_input.goal_text
    )

    # 3. Call the LLM using the structured output configuration (JSON Schema)
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=prompt,
            config=GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=TaskPlan,
                temperature=0.4 # Use a lower temperature for better reasoning/consistency
            ),
        )

        # 4. Parse and Validate Output
        # The response text is a guaranteed JSON string matching TaskPlan schema
        plan_data = json.loads(response.text)
        return TaskPlan(**plan_data)
        
    except Exception as e:
        # Log the error and any invalid LLM text for debugging
        print(f"LLM output parsing or API call failed: {e}")
        # In a real app, you would inspect response.text here if available
        raise ValueError("AI planning failed to produce a valid plan. Try a different prompt.")
