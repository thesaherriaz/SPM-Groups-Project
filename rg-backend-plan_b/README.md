# Research Genie – Backend

The **Research Genie Backend** powers the AI-based research paper summarization platform. This backend is built using **FastAPI**, **PostgreSQL**, and **SQLAlchemy** for scalability and performance.


## Tech Stack

| Component | Technology |
|------------|-------------|
| Language | Python 3.12 |
| Framework | FastAPI |
| Web Server | Uvicorn |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Environment Management | python-dotenv |
| Validation | Pydantic |


## Project Structure

```
rg_backend/
│
├── app/
│   ├── main.py                 # Entry point (FastAPI app + routes)
│   ├── config.py               # Configuration file
│   ├── controllers/            # Request/response handlers
│   ├── models/                 # Database models
│   ├── services/               # Business logic and helpers
│   └── database/
│       └── connection.py       # SQLAlchemy DB connection
│
├── .env                        # Environment variables
├── .gitignore                  # Ignored files/folders
├── requirements.txt            # Dependencies list
└── README.md                   # Documentation
```

## Installation & Setup

1. Clone the Repository
   git clone https://github.com/abubakarmunir712/research-genie-backend.git
   cd research-genie-backend

2. Create & Activate Virtual Environment
    ```
    python -m venv venv
    ```
    For Windows
    ```
    venv\Scripts\activate
    ```
    For macOS/Linux
    ```
    source venv/bin/activate
    ```

3. Install Dependencies
    ```
    pip install -r requirements.txt
    ```

4. Run the Server
    ```
    uvicorn app.main:app --reload
    ```

## Environment Variables (.env)

Create a .env file in the root directory and add:
```
DB_URL=postgresql://postgres:yourpassword@localhost:5432/research_genie
SECRET_KEY=your_secret_key_here
```

## Available Endpoints

Method: GET
Endpoint: /
Description: Root endpoint – confirms backend running

Method: GET
Endpoint: /health
Description: Health check API – verifies server status

Example Response (/health)
```
{
  "status": "ok",
  "message": "Backend running successfully"
}
```

## Current Features

- FastAPI backend setup and running
- Configured environment variables (.env)
- Database connection file prepared (SQLAlchemy)
- Health-check endpoint implemented
- Clean and modular project structure

## Sprints Progress

| Sprint | Description | Status |
|---------|--------------|---------|
| **Sprint 1** | Backend environment setup, FastAPI configuration, and initial API creation. | ✅ Completed |