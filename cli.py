import os
import warnings
import logging
import time

os.environ["PYTHONWARNINGS"] = "ignore"
warnings.filterwarnings("ignore")
logging.getLogger("google").setLevel(logging.ERROR)
logging.getLogger("google.genai").setLevel(logging.ERROR)

from google.genai.errors import APIError

import argparse
import sys
from evaluator import evaluate_text

parser = argparse.ArgumentParser(
    description="Evaluate historical text for historiographical framing flaws."
)
parser.add_argument(
    "text",
    type=str,
    nargs="?",
    help="The historical text passage to evaluate directly as a string.",
)
parser.add_argument(
    "--file",
    "-f",
    type=str,
    help="Path to a text file containing the passage to evaluate.",
)

args = parser.parse_args()

target_text = ""
if args.file:
    try:
        with open(args.file, "r", encoding="utf-8") as f:
            target_text = f.read().strip()
    except FileNotFoundError:
        print(f"Error: File not found at '{args.file}'.")
        sys.exit(1)
elif args.text:
    target_text = args.text.strip()

if not target_text:
    print("Error: No text provided. Pass a passage directly or use --file <path>.")
    sys.exit(1)

print("\nAnalyzing text for historiographical framing flaws...\n")
report = None
max_retries = 3
for attempt in range(max_retries):
    try:
        report = evaluate_text(target_text)
        break
    except APIError as e:
        if attempt < max_retries - 1:
            print(f"Server busy. Pausing 10s before retry (Attempt {attempt + 1}/{max_retries})...")
            time.sleep(10)
        else:
            raise e

print(f"Framing Flaws Detected: {report.has_framing_flaws}")
for flaw in report.detected_flaws:
    print(f"\n[{flaw.flaw_type.value}] - Severity: {flaw.severity}/5")
    print(f'  Quote: "{flaw.quote}"')
    print(f"  Critique: {flaw.explanation}")

print(f"\nOverall Assessment:\n{report.overall_assessment}")