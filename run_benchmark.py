import json
from datetime import datetime
from dataset import BENCHMARK_CASES
from evaluator import evaluate_text
from metrics import compute_benchmark_metrics


def save_benchmark_artifact(metrics, results, filename="benchmark_results.json"):
    payload = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "summary": metrics.model_dump(),
        "case_details": [
            {"passed": r["passed"], "report": r["report"].model_dump()}
            for r in results
        ],
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"\nArtifact saved to: {filename}")


def run_benchmark():
    print(f"Starting evaluation across {len(BENCHMARK_CASES)} benchmark cases...\n")
    results = []

    for case in BENCHMARK_CASES:
        print(f"Evaluating case: [{case.id}] ({case.historical_context})...")
        report = evaluate_text(case.text)
        is_passed = report.has_framing_flaws == case.should_have_flaws
        results.append({"passed": is_passed, "report": report})

    metrics = compute_benchmark_metrics(results)
    print("\n=== Benchmark Summary Metrics ===")
    print(f"Total Cases: {metrics.total_cases}")
    print(f"Passed Cases: {metrics.passed_cases}")
    print(f"Accuracy: {metrics.accuracy_percentage:.1f}%")
    print(f"Total Flaws Identified: {metrics.total_flaws_detected}")
    print(f"Average Flaw Severity: {metrics.average_severity:.2f}/5.0")
    print("Flaw Breakdown by Type:")
    for flaw, count in metrics.flaws_by_type.items():
        print(f"  - {flaw}: {count}")

    save_benchmark_artifact(metrics, results)
    return metrics


if __name__ == "__main__":
    run_benchmark()