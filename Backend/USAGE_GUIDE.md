# Research Methodology API - Usage Guide

## Overview

This API analyzes research questions and recommends appropriate research methodology, study design, and data collection tools using AI-powered analysis.

**Endpoint:** `POST /api/analyze-questions`  
**Base URL:** `http://localhost:5000`

## Getting Starte

```bash
python app.py
```

The server will start on `http://localhost:5000`

### 3. Make a Request

```bash
curl -X POST http://localhost:5000/api/analyze-questions \
  -H "Content-Type: application/json" \
  -d '{
    "main_question": "How does social media usage affect mental health in teenagers?",
    "sub_questions": [
      "What is the average daily screen time of teenagers?",
      "How do teenagers perceive their mental health?",
      "What coping mechanisms do teenagers use when stressed?"
    ]
  }'
```

---

## API Reference

### Request Format

**Method:** `POST`  
**URL:** `http://localhost:5000/api/analyze-questions`  
**Content-Type:** `application/json`

**Request Body:**
```json
{
  "main_question": "string (required, non-empty)",
  "sub_questions": ["string", "string", ...] (required, non-empty array)
}
```

**Validation Rules:**
- `main_question`: Required, must be a non-empty string
- `sub_questions`: Required, must be a non-empty array of non-empty strings

### Response Format

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Methodology analysis completed successfully",
  "data": {
    "questions": {
      "main_question": "How does social media usage affect mental health in teenagers?",
      "sub_questions": [
        "What is the average daily screen time of teenagers?",
        "How do teenagers perceive their mental health?",
        "What coping mechanisms do teenagers use when stressed?"
      ]
    },
    "methodology": {
      "recommended_methodology": "Mixed-methods (Sequential Explanatory Design)",
      "justification": "The main research question requires both quantitative data...",
      "study_design": "Sequential Explanatory Design: Phase 1 - Quantitative survey...",
      "data_collection_tools": "Phase 1: Online questionnaire with validated scales..."
    }
  }
}
```

**Error Response (400 Bad Request):**
```json
{
  "success": false,
  "message": "main_question cannot be empty",
  "data": null
}
```

**Server Error (500):**
```json
{
  "success": false,
  "message": "Internal server error: Connection timeout",
  "data": null
}
```

---

## Code Examples

### JavaScript (Fetch API)

```javascript
const response = await fetch('http://localhost:5000/api/analyze-questions', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    main_question: "How does remote work affect employee productivity?",
    sub_questions: [
      "What tools do remote workers use?",
      "How do they manage work-life balance?",
      "What are the productivity metrics?"
    ]
  })
});

const data = await response.json();

if (data.success) {
  console.log('Methodology:', data.data.methodology.recommended_methodology);
  console.log('Justification:', data.data.methodology.justification);
} else {
  console.error('Error:', data.message);
}
```

### Python (requests)

```python
import requests

response = requests.post(
    'http://localhost:5000/api/analyze-questions',
    json={
        "main_question": "How does remote work affect employee productivity?",
        "sub_questions": [
            "What tools do remote workers use?",
            "How do they manage work-life balance?",
            "What are the productivity metrics?"
        ]
    }
)

data = response.json()

if data['success']:
    methodology = data['data']['methodology']
    print(f"Methodology: {methodology['recommended_methodology']}")
    print(f"Justification: {methodology['justification']}")
else:
    print(f"Error: {data['message']}")
```

### cURL

```bash
curl -X POST http://localhost:5000/api/analyze-questions \
  -H "Content-Type: application/json" \
  -d '{
    "main_question": "What is the impact of AI tools on student learning outcomes?",
    "sub_questions": [
      "How frequently do students use AI tools?",
      "What types of AI tools are most popular?",
      "How do teachers perceive AI tools in education?"
    ]
  }'
```

---

## Testing

### Automated Test Suite

Run predefined test cases:
```bash
python test_analyze_questions.py
```

### Interactive Testing

Test with your own questions:
```bash
python test_interactive.py
```

### Health Check

Verify the server is running:
```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "Backend is running"
}
```

---

## Response Fields Explained

### `questions` Object
- **main_question**: Your primary research question (echoed back)
- **sub_questions**: Your sub-questions (echoed back)

### `methodology` Object
- **recommended_methodology**: The type of research methodology (e.g., "Mixed-methods", "Qualitative", "Quantitative")
- **justification**: Detailed explanation of why this methodology is appropriate for your research questions
- **study_design**: Specific research design approach (e.g., "Sequential Explanatory Design", "Convergent Parallel Design")
- **data_collection_tools**: Recommended tools and instruments for collecting data (surveys, interviews, analytics, etc.)

---

## Common Use Cases

### Example 1: Social Science Research
```json
{
  "main_question": "How does social media usage affect mental health in teenagers?",
  "sub_questions": [
    "What is the average daily screen time?",
    "How do teenagers perceive their mental health?",
    "What coping mechanisms do they use?"
  ]
}
```
**Expected Methodology:** Mixed-methods (combines quantitative screen time data with qualitative perceptions)

### Example 2: Business Research
```json
{
  "main_question": "How does remote work affect employee productivity?",
  "sub_questions": [
    "What collaboration tools are used most?",
    "How do employees manage work-life balance?",
    "What are the key productivity metrics?"
  ]
}
```
**Expected Methodology:** Mixed-methods (quantitative metrics + qualitative experiences)

### Example 3: Education Research
```json
{
  "main_question": "What is the impact of AI tools on student learning outcomes?",
  "sub_questions": [
    "How frequently do students use AI tools?",
    "What types of AI tools are most popular?",
    "How do teachers perceive AI tools?"
  ]
}
```
**Expected Methodology:** Mixed-methods or Explanatory Sequential Design

---

## Troubleshooting

### "Connection refused" error
- Ensure the server is running: `python app.py`
- Check the URL is correct: `http://localhost:5000`
- Verify port 5000 is not blocked by firewall

### "GEMINI_API_KEY not found" warning
- Create a `.env` file in the project root
- Add: `GEMINI_API_KEY=your_actual_api_key`
- Restart the server

### "Module not found" error
- Install dependencies: `pip install -r requirements.txt`
- Verify you're using Python 3.7+

### Slow responses (30+ seconds)
- This is normal - AI analysis takes time
- Gemini API typically responds in 5-30 seconds
- Consider using `gemini-2.5-flash` for faster responses

### "Model not found" error
- Update your `.env` file with: `GEMINI_MODEL=gemini-2.5-flash`
- Check available models at: https://ai.google.dev/models/gemini

---

## CORS Configuration

The API accepts requests from:
- `http://localhost:5173` (Vite)
- `http://localhost:3000` (React)
- `http://127.0.0.1:5173`

To add more origins, edit `app.py` and update the `CORS` configuration.

---

## Project Structure

```
Backend/
├── app.py                      # Main Flask application
├── services/
│   ├── gemini_service.py      # Gemini API integration
│   └── prompt_templates.py    # AI prompt templates
├── utils/
│   └── validator.py           # Input validation
├── .env                        # Environment variables (create this)
├── requirements.txt           # Python dependencies
└── USAGE_GUIDE.md            # This file
```

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify your setup with: `python check_setup.py`
3. Review the test examples: `python example_output.py`
4. Check Gemini API status: https://status.cloud.google.com/

---

## Notes

- The API uses Google Gemini AI for methodology recommendations
- Responses are AI-generated and may vary between requests
- All responses are in JSON format
- The endpoint is designed for research methodology analysis only
- Input validation ensures data quality before processing
