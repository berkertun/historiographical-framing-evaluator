import os
import time
import json
import logging
import warnings

# 1. Nuke all warnings at the system level BEFORE Google libraries load
os.environ["PYTHONWARNINGS"] = "ignore"
warnings.filterwarnings("ignore")
logging.getLogger("google").setLevel(logging.ERROR)
logging.getLogger("google.genai").setLevel(logging.ERROR)

from evaluator import evaluate_text
from dataset import BENCHMARK_CASES
from google.genai.errors import APIError

print("Starting Historiographical Batch Evaluation...\n")
saved_reports = []

for case in BENCHMARK_CASES:
    print(f"Evaluating case: {case.id}")
    
    # 2. Production-Grade Retry Loop
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Attempt to evaluate the text
            report = evaluate_text(case.text)
            passed = (report.has_framing_flaws == case.should_have_flaws)
            print(f"  Result: {'PASS ✅' if passed else 'FAIL ❌'}\n")
            
            # Save the successful result
            saved_reports.append({"case_id": case.id, "evaluation": report.model_dump()})
            break  # Success! Break out of the retry loop and move to the next case
            
        except APIError as e:
            # If Google yells at us to slow down, catch it and wait
            if "429" in str(e) or "503" in str(e):
                print(f"  [API Limit Hit] Server exhausted. Cooling down for 35 seconds (Attempt {attempt + 1}/{max_retries})...")
                time.sleep(35)
            else:
                # If it's a different kind of error, crash normally
                raise e
    
    # A small polite pause between normal successful requests
    time.sleep(5)

# 3. Save the final output
with open("final_reports.json", "w", encoding="utf-8") as file:
    json.dump(saved_reports, file, indent=2, ensure_ascii=False)

print("Evaluation complete! Detailed scholarly reports saved to final_reports.json")