from evaluator import evaluate_text

sample_text = (
    "The Tanzimat reforms of 1839 were an inevitable Westernization program "
    "intended to rescue a backwards, decaying Ottoman Empire from oriental stagnation. "
    "The reformers passively mimicked French constitutional ideals in a futile attempt "
    "to drag an unwilling, primitive society into the modern democratic era. "
    "Because the Porte lacked the moral maturity to properly adopt Western enlightenment, "
    "the reforms were doomed to fail from the start."
)

report = evaluate_text(sample_text)

print(f"\n--- Evaluation Results ---")
print(f"Framing Flaws Detected: {report.has_framing_flaws}\n")
for flaw in report.detected_flaws:
    print(f"[{flaw.flaw_type.value}]")
    print(f"  Quote: \"{flaw.quote}\"")
    print(f"  Critique: {flaw.explanation}\n")

print(f"Overall Assessment:\n{report.overall_assessment}")