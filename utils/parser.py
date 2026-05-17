import json
import re

def extract_json(text: str) -> dict:
    """
    Extracts JSON from a Gemini response string.
    Handles cases where the model wraps JSON in markdown code blocks.
    Returns an empty dict on failure.
    """
    try:
        # Remove markdown code fences if present (```json ... ```)
        cleaned = re.sub(r"```(?:json)?", "", text).replace("```", "").strip()
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Try to find JSON object using regex as a fallback
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except Exception:
                pass
        print("[Parser Error] Could not extract valid JSON from response.")
        return {}
