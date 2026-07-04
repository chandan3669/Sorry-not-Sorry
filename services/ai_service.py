import os

from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()

GEMINI_MODEL = "gemini-3.1-flash-lite"
GEMINI_TIMEOUT_SECONDS = 15


class AIServiceError(Exception):
    """Raised when excuse generation fails."""


def _build_multi_excuse_prompt(prompt: str) -> str:
    return (
        f"{prompt}\n\n"
        "Generate exactly 3 unique excuses. "
        "Separate each excuse using ###. "
        "Do not include numbering, labels, bullets, or extra commentary."
    )


def _parse_excuses(response_text: str) -> list[str]:
    excuses = [part.strip() for part in response_text.split("###")]
    excuses = [excuse for excuse in excuses if excuse]
    if len(excuses) != 3:
        raise AIServiceError("Gemini did not return exactly 3 excuses")
    return excuses


def generate_excuses(prompt: str) -> list[str]:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise AIServiceError("GEMINI_API_KEY not found")

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(GEMINI_MODEL)
        multi_excuse_prompt = _build_multi_excuse_prompt(prompt)

        for attempt in range(2):
            response = model.generate_content(
                multi_excuse_prompt,
                request_options={"timeout": GEMINI_TIMEOUT_SECONDS},
            )
            response_text = response.text.strip()
            if not response_text:
                if attempt == 0:
                    continue
                raise AIServiceError("Gemini returned an empty excuse")

            try:
                return _parse_excuses(response_text)
            except AIServiceError:
                if attempt == 0:
                    continue
                raise

        raise AIServiceError("Gemini did not return exactly 3 excuses")
    except AIServiceError:
        raise
    except Exception as exc:
        error_message = str(exc).lower()
        if "429" in error_message or "quota" in error_message:
            raise AIServiceError("Gemini quota or rate limit reached") from exc
        if "api key" in error_message or "permission" in error_message:
            raise AIServiceError("Gemini API key is invalid or does not have access") from exc
        if "timeout" in error_message or "deadline" in error_message:
            raise AIServiceError("Gemini request timed out") from exc
        raise AIServiceError("Gemini API Error") from exc
