import os

from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()

GEMINI_MODEL = "gemini-2.0-flash-lite"
GEMINI_TIMEOUT_SECONDS = 15


class AIServiceError(Exception):
    """Raised when excuse generation fails."""


def generate_excuse(prompt: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise AIServiceError("GEMINI_API_KEY not found")

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(
            prompt,
            request_options={"timeout": GEMINI_TIMEOUT_SECONDS},
        )
        excuse = response.text.strip()
        if not excuse:
            raise AIServiceError("Gemini returned an empty excuse")
        return excuse
    except AIServiceError:
        raise
    except Exception as exc:
        raise AIServiceError(f"Gemini API Error: {str(exc)}") from exc
