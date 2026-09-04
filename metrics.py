from pydantic import BaseModel
from schema import FramingEvaluationReport


class BenchmarkMetrics(BaseModel):
    total_cases: int
    passed_cases: int
    accuracy_percentage: float
    total_flaws_detected: int
    average_severity: float
    flaws_by_type: dict[str, int]


def compute_benchmark_metrics(results: list[dict]) -> BenchmarkMetrics:
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    acc = round((passed / total * 100.0), 2) if total else 0.0

    flaws = [f for r in results for f in r["report"].detected_flaws]
    avg_sev = round(sum(f.severity for f in flaws) / len(flaws), 2) if flaws else 0.0

    counts: dict[str, int] = {}
    for f in flaws:
        key = str(f.flaw_type.value)
        counts[key] = counts.get(key, 0) + 1

    return BenchmarkMetrics(
        total_cases=total,
        passed_cases=passed,
        accuracy_percentage=acc,
        total_flaws_detected=len(flaws),
        average_severity=avg_sev,
        flaws_by_type=counts,
    )