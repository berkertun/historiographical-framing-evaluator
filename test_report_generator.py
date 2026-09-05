from metrics import BenchmarkMetrics
from report_generator import generate_markdown_summary


def test_generate_markdown_summary_tables():
    mock_metrics = BenchmarkMetrics(
        total_cases=10,
        passed_cases=9,
        accuracy_percentage=90.0,
        total_flaws_detected=3,
        average_severity=3.5,
        flaws_by_type={"whig_teleology": 2, "agency_flattening": 1},
    )
    markdown_output = generate_markdown_summary(mock_metrics)

    assert "# Historiographical Framing Evaluation Report" in markdown_output
    assert "| Accuracy | 90.0% |" in markdown_output
    assert "| `whig_teleology` | 2 |" in markdown_output
    assert "| `agency_flattening` | 1 |" in markdown_output