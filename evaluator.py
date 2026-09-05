import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ServerError
from schema import FramingEvaluationReport

load_dotenv()

SYSTEM_INSTRUCTION = """You are an expert historiographical evaluator.
Analyze the provided text for teleological and conceptual framing flaws:
1. Whig Teleology: Treating historical developments as an inevitable march toward the modern state.
2. Eurocentric Developmentalism: Treating non-Western reforms as derivative copies of European models.
3. Anachronistic Moralism: Evaluating historical actors through modern ethical standards.
4. Agency Flattening: Treating historical actors as passive recipients of external influence.

For each flaw, provide verbatim quotes, scholarly explanations, and a severity score (1-5):
- 1: Incidental bias (minor uncritical phrasing; core analysis remains sound).
- 2: Latent bias (subtle developmental undertones under contextualized claims).
- 3: Moderate flaw (unexamined developmental assumptions diminish contingency).
- 4: Heavy distortion (teleological or Eurocentric framing drives the causal argument).
- 5: Pure caricature (blatant inevitability, moral condescension, or total erasure of agency)."""

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

PRIMARY_MODEL = "gemini-3.8-flash"
FALLBACK_MODEL = "gemini-3.5-flash-lite"


def evaluate_text(text: str, max_retries: int = 3) -> FramingEvaluationReport:
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        response_mime_type="application/json",
        response_schema=FramingEvaluationReport,
        temperature=0.0,
    )

    models_to_attempt = [PRIMARY_MODEL, FALLBACK_MODEL]

    for model_name in models_to_attempt:
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=f"Analyze this historical text for framing flaws:\n\n{text}",
                    config=config,
                )
                return response.parsed
            except ServerError as error:
                error_msg = str(error)
                if "503" in error_msg or "UNAVAILABLE" in error_msg:
                    wait_seconds = (2 ** attempt) * 2
                    print(
                        f"[Capacity Warning] {model_name} busy. "
                        f"Retrying in {wait_seconds}s (attempt {attempt + 1}/{max_retries})..."
                    )
                    time.sleep(wait_seconds)
                else:
                    raise error
            except Exception as error:
                print(f"[Error on {model_name}]: {error}")
                break

    raise RuntimeError("Evaluation failed: all model endpoints and retries were exhausted.")


if __name__ == "__main__":
    print("Gemini client successfully initialized.")