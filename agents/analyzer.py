from utils.gemini_client import call_gemini
from utils.parser import extract_json

def analyze_references(reference_text: str) -> dict:
    """
    Analyzes reference carousel text and returns a style profile as a dict.
    The style profile includes tone, hook style, CTA style, etc.
    """
    # Load the prompt template
    with open("prompts/analyzer_prompt.txt", "r") as f:
        prompt_template = f.read()

    # Fill in the reference text
    prompt = prompt_template.replace("{{REFERENCE_TEXT}}", reference_text)

    # Call Gemini
    response = call_gemini(prompt)

    if not response:
        return {}

    # Parse JSON from the response
    return extract_json(response)
