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
from metrics import compute_benchmark_metrics

print("Starting Historiographical Batch Evaluation...\n")
saved_reports = []
benchmark_results = []

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
            benchmark_results.append({
                "case_id": case.id,
                "passed": passed,
                "report": report
            })
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

# 3. Compute benchmark metrics
metrics = compute_benchmark_metrics(benchmark_results)

# 4. Save combined payload (metrics + qualitative reports) to disk
final_payload = {
    "metrics": metrics.model_dump(),
    "case_reports": saved_reports
}

with open("final_reports.json", "w", encoding="utf-8") as file:
    json.dump(final_payload, file, indent=2, ensure_ascii=False)

print("\n=== HISTORIOGRAPHICAL BENCHMARK SCORECARD ===")
print(f"Total Cases: {metrics.total_cases}")
print(f"Pass Rate: {metrics.accuracy_percentage}% ({metrics.passed_cases}/{metrics.total_cases})")
print(f"Total Flaws Detected: {metrics.total_flaws_detected}")
print(f"Average Severity: {metrics.average_severity}/5.0")
print("Flaws by Category:")
for flaw, count in metrics.flaws_by_type.items():
    print(f"  - {flaw}: {count}")

print("\nEvaluation complete! Structured benchmark data saved to final_reports.json")