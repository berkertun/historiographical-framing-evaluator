from metrics import BenchmarkMetrics, compute_benchmark_metrics
from run_benchmark import evaluate_quality_gate
from schema import FlawEvidence, FlawType, FramingEvaluationReport

def test_compute_benchmark_metrics_clean_pass():
    report = FramingEvaluationReport(
        has_framing_flaws=False,
        overall_assessment="Historically sound analysis.",
        detected_flaws=[],
    )
    mock_results = [{"passed": True, "report": report}]
    metrics = compute_benchmark_metrics(mock_results)

    assert metrics.total_cases == 1
    assert metrics.passed_cases == 1
    assert metrics.accuracy_percentage == 100.0
    assert metrics.total_flaws_detected == 0
    assert metrics.average_severity == 0.0

    from schema import FlawEvidence, FlawType


def test_compute_benchmark_metrics_with_flaws():
    flaw_1 = FlawEvidence(
        flaw_type=FlawType.EUROCENTRIC_DEVELOPMENTALISM,
        severity=4,
        quote="copied European models",
        explanation="Eurocentric assumption.",
    )
    flaw_2 = FlawEvidence(
        flaw_type=FlawType.AGENCY_FLATTENING,
        severity=2,
        quote="passive subjects",
        explanation="Erases agency.",
    )
    report = FramingEvaluationReport(
        has_framing_flaws=True,
        overall_assessment="Flawed.",
        detected_flaws=[flaw_1, flaw_2],
    )
    metrics = compute_benchmark_metrics([{"passed": True, "report": report}])

    assert metrics.total_flaws_detected == 2
    assert metrics.average_severity == 3.0
    assert metrics.flaws_by_type["eurocentric_developmentalism"] == 1
    assert metrics.flaws_by_type["agency_flattening"] == 1

def test_evaluate_quality_gate_thresholds():
    mock_metrics = BenchmarkMetrics(
        total_cases=10,
        passed_cases=8,
        accuracy_percentage=80.0,
        total_flaws_detected=0,
        average_severity=0.0,
        flaws_by_type={},
    )
    assert evaluate_quality_gate(mock_metrics, threshold=80.0) is True
    assert evaluate_quality_gate(mock_metrics, threshold=85.0) is False
    assert evaluate_quality_gate(mock_metrics, threshold=75.0) is True