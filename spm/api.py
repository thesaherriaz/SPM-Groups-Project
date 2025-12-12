import requests
import json

# ------------------------------------------------------------
# 1. LOCAL API (Research Gaps)
# ------------------------------------------------------------
def test_local_api(topic):
    url = "http://localhost:8000/researchgap"
    params = {"query": topic}

    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()
        print("\n=== Local API Response ===")
        print(json.dumps(data, indent=2))
        return data

    except requests.exceptions.RequestException as e:
        print("Error connecting to Local API:", e)
        return {}


# ------------------------------------------------------------
# 2. EXTERNAL API (Generate Research Questions)
# ------------------------------------------------------------
def test_external_api(topic, gaps):
    if not gaps or "gaps" not in gaps or len(gaps["gaps"]) == 0:
        print("No gaps found to send to external API.")
        return {}

    # Convert gaps into required format
    gaps_payload = [
        {
            "gap_id": f"gap_{i+1}",
            "description": gap["statement"],
            "category": "methodological_gap"
        }
        for i, gap in enumerate(gaps["gaps"])
    ]

    url = f"https://spm-production.up.railway.app/generateQuestions?topic={topic}"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(gaps_payload), timeout=20)
        response.raise_for_status()
        data = response.json()
        print("\n=== External API Response ===")
        print(json.dumps(data, indent=2))
        return data

    except requests.exceptions.RequestException as e:
        print("Error connecting to External API:", e)
        return {}


# ------------------------------------------------------------
# 3. RESEARCH METHODOLOGY API (Your Flask App)
# ------------------------------------------------------------
def test_methodology_api(question_data):
    if not question_data or "data" not in question_data:
        print("Invalid question data. Cannot call methodology API.")
        return {}

    main_question = question_data["data"]["main_question"]
    sub_questions = question_data["data"]["sub_questions"]

    url = "http://127.0.0.1:5000/api/analyze-questions"
    payload = {
        "main_question": main_question,
        "sub_questions": sub_questions
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        print("\n=== Research Methodology API Response ===")
        print(json.dumps(data, indent=2))
        return data

    except requests.exceptions.RequestException as e:
        print("Error connecting to Research Methodology API:", e)
        return {}


# ------------------------------------------------------------
# MAIN WORKFLOW
# ------------------------------------------------------------
if __name__ == "__main__":
    topic = "data engineering in healthcare"

    # Step 1: Call Local API
    gaps_data = test_local_api(topic)

    # Step 2: Send gaps → External API
    questions_data = test_external_api(topic, gaps_data)

    # Step 3: Send questions → Methodology API
    test_methodology_api(questions_data)
