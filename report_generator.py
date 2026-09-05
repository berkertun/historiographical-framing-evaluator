from metrics import BenchmarkMetrics


def generate_markdown_summary(metrics: BenchmarkMetrics) -> str:
    md = "# Historiographical Framing Evaluation Report\n\n"
    md += "## Summary Metrics\n\n"
    md += "| Metric | Value |\n"
    md += "| :--- | :--- |\n"
    md += f"| Total Test Cases | {metrics.total_cases} |\n"
    md += f"| Passed Cases | {metrics.passed_cases} |\n"
    md += f"| Accuracy | {metrics.accuracy_percentage:.1f}% |\n"
    md += f"| Total Flaws Found | {metrics.total_flaws_detected} |\n"
    md += f"| Average Severity | {metrics.average_severity:.2f} / 5.0 |\n\n"
    md += "### Flaw Distribution by Category\n\n"
    md += "| Category | Occurrences |\n"
    md += "| :--- | :--- |\n"
    for flaw_type, count in metrics.flaws_by_type.items():
        md += f"| `{flaw_type}` | {count} |\n"
    md += "\n"
    return md