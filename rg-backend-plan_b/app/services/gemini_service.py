import json
import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.gemini_api_key)


def get_research_gaps(query: str) -> dict:
    """
    Uses Gemini to generate 5 research gaps for the user query.
    Returns JSON like:
    {
        "gaps": [
            {"statement": "Gap 1", "score": 95},
            {"statement": "Gap 2", "score": 87},
            ...
        ]
    }
    """
    prompt = f"""
    You are an AI assistant. Analyze the following academic topic and identify 5 potential research gaps.
    Each gap should have an importance score from 1 to 100 (100 = most important).
    Respond ONLY in JSON format like this:

    {{
        "gaps": [
            {{"statement": "Gap description 1", "score": 95}},
            {{"statement": "Gap description 2", "score": 87}},
            {{"statement": "Gap description 3", "score": 80}},
            {{"statement": "Gap description 4", "score": 75}},
            {{"statement": "Gap description 5", "score": 70}}
        ]
    }}

    Topic: "{query}"
    """

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=0.3),
        )

        text = response.text.strip()

        # Clean code fences or quotes if present
        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()
        elif text.startswith('"') and text.endswith('"'):
            text = text[1:-1]

        data = json.loads(text)
        return data

    except json.JSONDecodeError:
        return {"gaps": [], "message": "Gemini did not return valid JSON"}
    except Exception as e:
        return {"gaps": [], "message": f"Something went wrong: {e}"}


def is_relevant_query(query: str) -> dict:
    prompt = f"""
    You are an AI assistant. Analyze this user query and respond ONLY in JSON format.
    The JSON should contain three fields:
    {{
        "relevant": true or false,
        "safe": true or false,
        "message": "Explanation if the query is not relevant or not safe"
    }}

    User Query: "{query}"
    """

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=0),
        )

        # Strip extra whitespace/newlines
        text = response.text.strip()

        # Sometimes Gemini wraps JSON in backticks or quotes, remove them
        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()
        elif text.startswith('"') and text.endswith('"'):
            text = text[1:-1]

        # Parse JSON safely
        data = json.loads(text)
        return {
            "relevant": data.get("relevant", False),
            "safe": data.get("safe", False),
            "message": data.get("message", ""),
        }

    except json.JSONDecodeError:
        # Return fallback if Gemini output is not valid JSON
        return {
            "relevant": False,
            "safe": False,
            "message": "Gemini did not return valid JSON",
        }
    except Exception as e:
        return {
            "relevant": False,
            "safe": False,
            "message": f"Something went wrong: {e}",
        }
