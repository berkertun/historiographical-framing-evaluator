import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from schema import FramingEvaluationReport

load_dotenv()

SYSTEM_INSTRUCTION = """You are an expert historiographical evaluator.
Analyze the provided text for teleological and conceptual framing flaws:
1. Whig Teleology: Treating historical developments as an inevitable march toward the modern state.
2. Eurocentric Developmentalism: Treating non-Western reforms as mere imitation of European models rather than localized institutional adaptations.
3. Anachronistic Moralism: Evaluating historical actors through modern ethical standards rather than contemporary horizon of expectations.
4. Agency Flattening: Treating historical actors as passive recipients of external influence rather than strategic innovators.
Extract verbatim quotes for each flaw found and provide scholarly explanations."""

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

if __name__ == "__main__":
    print("Gemini client successfully initialized.")