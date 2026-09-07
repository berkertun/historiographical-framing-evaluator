import json
import sys
from datetime import datetime
from dataset import BENCHMARK_CASES
from evaluator import evaluate_text
from metrics import compute_benchmark_metrics
from report_generator import generate_markdown_summary
from metrics import BenchmarkMetrics


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


def save_markdown_artifact(metrics, filename="benchmark_report.md"):
    report_text = generate_markdown_summary(metrics)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(f"Markdown report saved to: {filename}")


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
    save_markdown_artifact(metrics)

    return metrics

def evaluate_quality_gate(metrics: BenchmarkMetrics, threshold: float = 80.0) -> bool:
    return metrics.accuracy_percentage >= threshold
if __name__ == "__main__":
    MIN_ACCURACY_THRESHOLD = 80.0
    benchmark_metrics = run_benchmark()
    if not evaluate_quality_gate(benchmark_metrics, MIN_ACCURACY_THRESHOLD):
        print(
            f"\n[FAILURE] Accuracy {benchmark_metrics.accuracy_percentage:.1f}% "
            f"fell below required threshold of {MIN_ACCURACY_THRESHOLD:.1f}%."
        )
        sys.exit(1)
    print(f"\n[SUCCESS] Evaluation passed quality gate (>= {MIN_ACCURACY_THRESHOLD:.1f}%).")
    sys.exit(0)