import json
from utils.gemini_client import call_gemini
from utils.parser import extract_json

def review_carousel(carousel: dict, style_profile: dict) -> dict:
    """
    Reviews the generated carousel and improves weak slides.
    Checks for: long slides, weak hooks, repeated points, off-brand tone.
    Returns improved carousel as a dict.
    """
    # Load the prompt template
    with open("prompts/reviewer_prompt.txt", "r") as f:
        prompt_template = f.read()

    # Fill in variables
    prompt = prompt_template.replace("{{CAROUSEL_JSON}}", json.dumps(carousel, indent=2))
    prompt = prompt.replace("{{STYLE_PROFILE}}", json.dumps(style_profile, indent=2))

    # Call Gemini
    response = call_gemini(prompt)

    if not response:
        return {}

    return extract_json(response)
