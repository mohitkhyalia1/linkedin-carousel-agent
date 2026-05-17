import json
from utils.gemini_client import call_gemini
from utils.parser import extract_json

def write_carousel(topic: str, style_profile: dict, num_slides: int) -> dict:
    """
    Generates a full carousel based on the topic and extracted style profile.
    Returns a dict with a list of slides.
    """
    # Load the prompt template
    with open("prompts/writer_prompt.txt", "r") as f:
        prompt_template = f.read()

    # Fill in variables
    prompt = prompt_template.replace("{{TOPIC}}", topic)
    prompt = prompt.replace("{{STYLE_PROFILE}}", json.dumps(style_profile, indent=2))
    prompt = prompt.replace("{{NUM_SLIDES}}", str(num_slides))

    # Call Gemini
    response = call_gemini(prompt)

    if not response:
        return {}

    return extract_json(response)
