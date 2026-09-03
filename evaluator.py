import os
from dotenv import load_dotenv
from google import genai
from schema import FramingEvaluationReport

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

if __name__ == "__main__":
    print("Gemini client successfully initialized.")