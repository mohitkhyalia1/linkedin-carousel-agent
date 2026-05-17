import os
from pathlib import Path
import google.generativeai as genai


def load_env_file():
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if not env_path.exists():
        return

    with env_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and value and key not in os.environ:
                os.environ[key] = value


def get_api_key():
    load_env_file()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets.get("GEMINI_API_KEY")
        except Exception:
            api_key = None
    return api_key


# Configure the Gemini client using the API key from environment, .env, or Streamlit secrets
def get_model():
    api_key = get_api_key()
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable or Streamlit secret is not set.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-flash-latest")

def call_gemini(prompt: str) -> str:
    """
    Sends a prompt to Gemini and returns the response text.
    Returns empty string on failure.
    """
    try:
        model = get_model()
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        error_msg = f"[Gemini Error] {type(e).__name__}: {str(e)}"
        print(error_msg)
        # Try to provide more context
        try:
            import streamlit as st
            st.session_state.last_gemini_error = error_msg
        except:
            pass
        return ""
