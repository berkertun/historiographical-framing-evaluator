from evaluator import evaluate_text

control_text = (
    "The Tanzimat reforms of 1839 represented an adaptive reorganization "
    "of Ottoman imperial administration, negotiated by bureaucratic elites responding "
    "to internal fiscal strains, regional revolts, and international diplomatic pressures. "
    "Rather than merely importing foreign templates, reformers synthesized Islamic legal "
    "traditions with European administrative mechanisms to reassert state sovereignty "
    "within their own contemporary horizon of expectations."
)

report = evaluate_text(control_text)

print(f"\n--- Control Test Results ---")
print(f"Framing Flaws Detected: {report.has_framing_flaws}")
print(f"Flaw Count: {len(report.detected_flaws)}")
print(f"\nOverall Assessment:\n{report.overall_assessment}")