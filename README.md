# SPM Group Project

## Prerequisites

Before running the project, you need to set up your Gemini API key in the `.env` file for each of the three directories:
- `rg-backend-plan_b/`
- `Backend/`
- `spm/`

## Setup Instructions

### 1. Configure API Keys

Create a `.env` file in each directory and add your Gemini API key:

```
GEMINI_API_KEY=your_api_key_here
```

### 2. Running the Services

#### rg-backend-plan_b

Navigate to the directory and run:

```bash
cd rg-backend-plan_b
uvicorn app.main:app --reload --port 8000
```

#### Backend

Navigate to the directory and run both commands in separate terminals:

**Terminal 1:**
```bash
cd Backend
python app.py
```

**Terminal 2:**
```bash
cd Backend
flask run
```

#### spm

Navigate to the directory and run:

```bash
cd spm
python app.py
```

## Project Structure

```
SPM Group Project/
├── rg-backend-plan_b/    # FastAPI backend service (Port 8000)
├── Backend/              # Flask backend service
└── spm/                  # Main application
```

## Notes

- Ensure all dependencies are installed before running each service
- Make sure the required ports are available (8000 for FastAPI, default Flask port for Backend)
- All three services need to be running simultaneously for the full application to work
