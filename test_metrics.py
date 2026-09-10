from metrics import BenchmarkMetrics, compute_benchmark_metrics, evaluate_quality_gate, generate_markdown_summary
from run_benchmark import evaluate_quality_gate
from schema import FlawEvidence, FlawType, FramingEvaluationReport
from dataset import BenchmarkCase

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

def test_compute_benchmark_metrics_sensitivity_and_specificity():
    case_pos = BenchmarkCase(id="pos", historical_context="ctx", text="txt", should_have_flaws=True)
    case_neg = BenchmarkCase(id="neg", historical_context="ctx", text="txt", should_have_flaws=False)
    mock_rep = FramingEvaluationReport(
        has_framing_flaws=False,
        detected_flaws=[],
        overall_assessment="Historiographically sound text.",
    )
    results = [
        {"passed": True, "report": mock_rep, "case": case_pos},
        {"passed": False, "report": mock_rep, "case": case_pos},
        {"passed": True, "report": mock_rep, "case": case_neg},
    ]
    metrics = compute_benchmark_metrics(results)
    assert metrics.sensitivity_percentage == 50.0
    assert metrics.specificity_percentage == 100.0

def test_generate_markdown_summary():
    metrics = BenchmarkMetrics(
        total_cases=10,
        passed_cases=8,
        accuracy_percentage=80.0,
        sensitivity_percentage=75.0,
        specificity_percentage=85.0,
        total_flaws_detected=3,
        average_severity=2.5,
        flaws_by_type={"eurocentric_developmentalism": 2, "whig_teleology": 1},
    )
    summary_md = generate_markdown_summary(metrics)
    assert "| Accuracy | 80.0% |" in summary_md
    assert "| Sensitivity (Flaw Detection) | 75.0% |" in summary_md
    assert "| Specificity (Control Clearance) | 85.0% |" in summary_md