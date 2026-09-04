import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
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

def evaluate_text(text: str) -> FramingEvaluationReport:
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        response_mime_type="application/json",
        response_schema=FramingEvaluationReport,
        temperature=0.0,
    )
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"Analyze this historical text for framing flaws:\n\n{text}",
        config=config,
    )
    return response.parsed

if __name__ == "__main__":
    print("Gemini client successfully initialized.")