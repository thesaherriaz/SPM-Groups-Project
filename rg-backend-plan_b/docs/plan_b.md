# Research Genie Backend - Plan B API Docs 🚀

This doc explains how our Plan B backend works, how to run it, and what to expect when calling the API.

---

## 0. Setup & Run

1. Clone the repo:
```bash
git clone https://github.com/abubakarmunir712/rg-backend/
cd rg-backend
````

2. Fetch origin and switch to Plan B branch:

```bash
git fetch origin
git checkout plan_b
```

3. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

4. Install requirements:

```bash
pip install -r requirements.txt
```

5. Configure .env

```bash
cp .env.example .env
# Replace GEMINI_API_KEY in .env
```

6. Run the server:

```bash
uvicorn app.main:app --reload
```

API should now be running at `http://127.0.0.1:8000/`.

---

## 1. How Plan B Works 🛠️

1. **Query check:**

   * When you send a topic, the backend first calls `is_relevant_query` using Gemini.
   * Gemini checks if the query is:

     * Related to academic research gap finding
     * Safe (no inappropriate or harmful content)
   * Gemini returns a JSON with `relevant`, `safe`, and a `message`.

2. **Generating gaps:**

   * If the query passes, `get_research_gaps` is called.
   * Gemini analyzes the topic and generates **5 research gaps**.
   * Each gap comes with an **importance score (1–100)**.
   * Response is always in clean JSON like:

```json
{
  "gaps": [
    {"statement": "Gap description 1", "score": 95},
    {"statement": "Gap description 2", "score": 90},
    ...
  ]
}
```

3. **Error handling:**

   * Unsafe or irrelevant queries return a 400 with Gemini’s explanation.
   * If something goes wrong with Gemini, backend returns an empty gaps list plus an error message.

---

## 2. Endpoints

### `GET /`

* Quick check if backend is alive.

```json
{
  "message": "Welcome to Research Genie API"
}
```

### `GET /health`

* Health check.

```json
{
  "status": "ok",
  "message": "Backend running successfully"
}
```

### `POST /research-gaps`

* Send a research topic, get 5 gaps.

**Request Body**

```json
{
  "query": "AI in healthcare applications"
}
```

**Successful Response**

```json
{
  "gaps": [
    {"statement": "Gap in personalized AI diagnosis systems", "score": 95},
    {"statement": "Lack of research on AI explainability in healthcare", "score": 90},
    {"statement": "Limited studies on AI adoption barriers in hospitals", "score": 85},
    {"statement": "Insufficient evaluation of AI-based treatment plans", "score": 80},
    {"statement": "Gap in ethical frameworks for AI in medicine", "score": 75}
  ]
}
```

**Error Response (unsafe/irrelevant query)**

```json
{
  "detail": "Explanation why the query is invalid or unsafe"
}
```

---

## 3. Models

**Request Model**

```python
class ResearchGapRequest(BaseModel):
    query: str
```

**Response Model**

```python
class GapItem(BaseModel):
    statement: str
    score: int

class ResearchGapResponse(BaseModel):
    gaps: List[GapItem]
```

---

## 4. Notes for the Team

* Always send JSON with the `"query"` key.
* Response is ready-to-use JSON — just take the `gaps` list.
* Scores range **1–100**, where 100 = most important.
* Backend automatically handles irrelevant or unsafe queries.
* You can parse `gaps` directly for frontend display, analytics, or further processing.