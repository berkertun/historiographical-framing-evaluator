import os
from dotenv import load_dotenv

# Parse the .env file and inject its values into system environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key and not api_key.startswith("your_actual"):
    print("Environment configuration verified: GEMINI_API_KEY loaded successfully.")
else:
    print("Error: GEMINI_API_KEY is missing or contains placeholder text.")
    