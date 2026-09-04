from evaluator import evaluate_text
from dataset import BENCHMARK_CASES

print("Starting Historiographical Batch Evaluation...\n")

for case in BENCHMARK_CASES:
    print(f"Evaluating case: {case.id}")
    report = evaluate_text(case.text)
    
    # Check if the evaluator's finding matches our ground truth expectation
    passed = (report.has_framing_flaws == case.should_have_flaws)
    
    print(f"  Expected Flaws: {case.should_have_flaws} | Detected Flaws: {report.has_framing_flaws}")
    print(f"  Result: {'PASS ✅' if passed else 'FAIL ❌'}\n")