# Task List API (Pre-built App for Lab 2)

This is a small **pre-built FastAPI task list application** for **Software Requirements Engineering Lab 2**.

The idea is that the group starts from this base application, then **each student creates their own Git branch**, implements **one feature**, and submits a **merge request / pull request** back to the main branch.

## What this starter app already has

This pre-built app includes:

- create a task
- get all tasks
- get one task by ID
- update a task
- delete a task
- input validation using Pydantic
- automatic Swagger documentation using FastAPI

## Suggested features for students to add

Each student should implement **one different feature** in their own branch. Examples:

- due dates
- search tasks
- priority levels
- category/tag support
- filtering completed vs incomplete tasks
- assign task owner

## Project structure

```text
 task-list-prebuilt-app/
 ├── main.py
 ├── requirements.txt
 ├── .gitignore
 └── README.md
```

## Requirements

- Python 3.10 or later recommended
- pip

## Installation and running the app

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd task-list-prebuilt-app
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Run the application

```bash
uvicorn main:app --reload
```

The app will start on:

```text
http://127.0.0.1:8000
```

## 5. Open the API docs

FastAPI automatically provides Swagger UI.

Open:

```text
http://127.0.0.1:8000/docs
```

You can test every endpoint directly in the browser by clicking **Try it out**.

---

# API Overview

## Base endpoints in the starter app

### 1. Health check

**GET** `/`

Returns a simple response showing that the API is running.

### 2. Create a task

**POST** `/tasks`

Example JSON body:

```json
{
  "title": "Finish SRE lab",
  "description": "Prepare Task 2 group project"
}
```

### 3. Get all tasks

**GET** `/tasks`

Returns a list of all tasks.

### 4. Get one task

**GET** `/tasks/{task_id}`

Example:

```text
GET /tasks/1
```

### 5. Update a task

**PATCH** `/tasks/{task_id}`

Example JSON body:

```json
{
  "completed": true
}
```

Or:

```json
{
  "title": "Finish SRE lab report",
  "description": "Update screenshots and Git steps",
  "completed": false
}
```

### 6. Delete a task

**DELETE** `/tasks/{task_id}`

Example:

```text
DELETE /tasks/1
```

---

# Validation and error handling

This starter app already includes:

- task title must be at least 2 characters
- task title cannot exceed 100 characters
- description cannot exceed 300 characters
- task ID must be greater than 0
- 404 error if a task does not exist

---

# Step-by-step test instructions

## Test 1: Start the server

```bash
uvicorn main:app --reload
```

## Test 2: Open Swagger UI

Open:

```text
http://127.0.0.1:8000/docs
```

## Test 3: Create a task

Use **POST** `/tasks` with:

```json
{
  "title": "Finish report",
  "description": "Complete the group write-up"
}
```

## Test 4: View all tasks

Use **GET** `/tasks`

## Test 5: View one task

Use **GET** `/tasks/1`

## Test 6: Update a task

Use **PATCH** `/tasks/1`

```json
{
  "completed": true
}
```

## Test 7: Delete a task

Use **DELETE** `/tasks/1`

## Test 8: Test invalid data

Try creating a task with a one-letter title:

```json
{
  "title": "A",
  "description": "Invalid title"
}
```

This should return a validation error.

---

# Example cURL commands

## Create task

```bash
curl -X POST "http://127.0.0.1:8000/tasks" \
-H "Content-Type: application/json" \
-d '{
  "title": "Finish report",
  "description": "Complete the group write-up"
}'
```

## Get all tasks

```bash
curl "http://127.0.0.1:8000/tasks"
```

## Get one task

```bash
curl "http://127.0.0.1:8000/tasks/1"
```

## Update task

```bash
curl -X PATCH "http://127.0.0.1:8000/tasks/1" \
-H "Content-Type: application/json" \
-d '{
  "completed": true
}'
```

## Delete task

```bash
curl -X DELETE "http://127.0.0.1:8000/tasks/1"
```

---

# Git and collaboration workflow for the lab

## 1. Create the group repository

One person creates the GitHub repository and pushes this starter app.

## 2. Each student creates their own branch

Example:

```bash
git checkout -b feature/due-dates-kangwa
```

Other examples:

```bash
git checkout -b feature/search-tasks
```

```bash
git checkout -b feature/priority-levels
```

## 3. Each student implements one feature

Examples:

- Student A: due dates
- Student B: search
- Student C: priority

## 4. Commit the feature

```bash
git add .
git commit -m "Add due dates feature"
```

## 5. Push the branch

```bash
git push -u origin feature/due-dates-kangwa
```

## 6. Open a Pull Request / Merge Request

On GitHub:

- open the repository
- click **Compare & pull request**
- target branch should be `main`
- submit the request for review

---

# Suggested feature design examples

## Example 1: Due dates
Add a `due_date` field to tasks.

## Example 2: Search
Allow:

```text
GET /tasks?search=report
```

## Example 3: Priority
Add a field like:

```text
Low | Medium | High
```

---

# What to submit for Task 2

Each student should submit:

- their branch name
- the feature they implemented
- screenshots of the app/docs working
- screenshot of their pull request / merge request
- short explanation of what changed

---

# Important note

The starter app uses **in-memory storage only**, which means tasks are lost when the server stops.
This is fine for the lab because the focus is on:

- extending a pre-built application
- version control workflow
- branching
- merging
- feature implementation

If needed later, the group can replace this with a database.
