from dataset import BENCHMARK_CASES, BenchmarkCase


def test_benchmark_cases_integrity():
    assert len(BENCHMARK_CASES) > 0, "Benchmark cases list cannot be empty."

    for case in BENCHMARK_CASES:
        assert isinstance(case, BenchmarkCase)
        assert len(case.id.strip()) > 0, "Case ID must not be empty."
        assert len(case.historical_context.strip()) > 0, "Context must not be empty."
        assert len(case.text.strip()) > 20, "Passage text must be substantive."
        assert isinstance(case.should_have_flaws, bool), "Flag must be boolean."

def test_benchmark_cases_unique_ids():
    case_ids = [case.id for case in BENCHMARK_CASES]
    assert len(case_ids) == len(set(case_ids)), (
        f"Duplicate case IDs found: {set([x for x in case_ids if case_ids.count(x) > 1])}"
    )