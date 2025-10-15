# Smart-task-planner
The Smart Task Planner project leverages Large Language Model (LLM) reasoning to function as a digital project manager.Its main objective is to eliminate the manual effort required for project decomposition and scheduling by intelligently parsing a single input goal.

This project implements a **Smart Task Planner API** that transforms a user's high-level goal (e.g., "Launch a personal website in two weeks") into a detailed, structured project plan. It uses a **Large Language Model (LLM)** to perform the complex reasoning required for project management, generating a list of actionable tasks, estimated durations, dependencies, and calculated deadlines.

This system directly addresses the assignment requirements by focusing on:
* **AI Reasoning:** Leveraging the LLM for logical task generation and dependency mapping.
* **Structured Output:** Ensuring clear, machine-readable JSON output using Pydantic schemas.
* **Timeline Logic:** Calculating deadlines based on a starting date and task dependencies.

## 2. Technical Stack and Architecture

| Component | Technology | Role in Project |
| :--- | :--- | :--- |
| **Backend API** | Python (FastAPI) | High-performance API layer for handling requests and routing them to the LLM service. |
| **LLM Interface** | `google-genai` SDK | Communicates with the Gemini API to execute the planning prompt and enforce the JSON output structure. |
| **Data Validation** | Pydantic | Defines strict schemas for both the input (`GoalInput`) and the complex output (`TaskPlan`), ensuring reliable data exchange. |
| **Frontend (Optional)** | HTML, CSS, JavaScript | A simple UI to input the goal and dynamically display the generated task plan. |

## 3. LLM Usage and Prompt Design (Evaluation Focus: LLM Reasoning)

The core functionality of the Smart Task Planner lies in its LLM prompt, which instructs the model to act as an expert project manager. This prompt is critical for ensuring **Task Completeness** and **Timeline Logic** in the output.

### System Instruction / Role Assignment

The prompt is structured to force Chain-of-Thought (CoT) reasoning for highly consistent, logical outputs.

```text
You are an expert Project Manager AI. Your job is to break down the user's high-level goal into a series of detailed, actionable tasks.

CRITICAL INSTRUCTIONS:
1.  **Strict JSON Output**: You MUST respond ONLY with a single JSON object that strictly adheres to the provided TaskPlan schema. Do not include any conversational text, explanations, or markdown outside the JSON block.
2.  **Tasks**: Create a logical, sequential list of tasks (5 to 10 tasks minimum for a complex goal).
3.  **Timeline Logic**: The estimated_duration_days must logically result in the suggested_deadline, considering dependencies and the CURRENT_DATE.
4.  **Dependencies**: Define task dependencies using task IDs (e.g., Task 3 depends on Task 2). Task 1 usually has no dependencies.
5.  **Date Calculation**: Use the CURRENT_DATE as the starting point. All suggested_deadlines must be in YYYY-MM-DD format.
