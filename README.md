# Historiographical & Teleological Framing Evaluator

An automated evaluation harness designed to detect structural historiographical distortions—such as Whig teleology, Eurocentric developmentalism, anachronistic moralism, and historical agency flattening—in large language model outputs.

Built using Python, Pydantic, and the official Google GenAI SDK `google-genai`), this harness leverages native structured schema generation, deterministic sampling `temperature=0.0`), and calibrated negative control cases to evaluate historical analysis of 19th-century institutional reforms and conceptual change.

---

## Why This Evaluator Exists

Standard evaluation benchmarks for historical reasoning primarily measure factual retrieval (dates, treaty names, sequence of events). However, advanced language models frequently generate factually accurate narratives that remain historiographically defective:

* **Teleological Inevitability:** Treating modern nation-state institutions as the foreordained destination of historical change.

* **Eurocentric Developmentalism:** Depicting non-Western institutional reforms (e.g., the Ottoman Tanzimat or the codification of the *Mecelle*) as derivative, delayed, or flawed copies of European precedents.

* **Flattened Agency:** Framing historical actors as passive recipients of external Western influence rather than strategic innovators responding to internal dynamics and regional pressures.

* **Anachronistic Moralism:** Imposing contemporary ethical standards retrospectively onto historical contexts.

This harness operationalizes historiographical criticism into a typed, automated evaluation pipeline.

---

## Flaw Taxonomy & Calibrated Severity Rubric

The evaluator inspects historical text against four specific failure modes:

| Flaw Type | Target Conceptual Distortion |

| :--- | :--- |

| `whig_teleology` | Presenting history as an inevitable, linear march toward modern enlightenment or statehood. |

| `eurocentric_developmentalism` | Assessing non-Western institutions solely by their proximity to European models. |

| `anachronistic_moralism` | Judging historical actors using contemporary moral frameworks rather than their contemporary horizons. |

| `agency_flattening` | Treating historical figures and societies as passive objects acted upon by foreign dynamics. |

### Severity Scale (1–5)

Each identified flaw receives an exact quote, an analytical critique, and a severity score anchored to specific criteria:

* **1 - Incidental Bias:** Minor uncritical phrasing; the core causal argument remains historically grounded.

* **2 - Latent Bias:** Subtle developmental undertones embedded beneath contextualized historical claims.

* **3 - Moderate Flaw:** Unexamined developmental or teleological assumptions that diminish contingency.

* **4 - Heavy Distortion:** Teleological or Eurocentric framing forms the primary causal explanation.

* **5 - Pure Caricature:** Total erasure of agency, blatant inevitability, or overt moral condescension.

---

## System Architecture

The harness relies on three core design principles:

1. **Native Structured Outputs:** Enforces schema conformity at the API level via `types.GenerateContentConfig(response_mime_type="application/json", response_schema=FramingEvaluationReport)` instead of brittle post-hoc regex or markdown stripping.

2. **Resilience & Model Cascade:** Uses `gemini-3.8-flash` as the primary reasoning engine, with exponential backoff for transient capacity spikes `503 UNAVAILABLE`) and an automated fallback to `gemini-3.5-flash-lite` if rate limits `429 RESOURCE_EXHAUSTED`) are reached.

3. **Hermetic Test Suite:** Offline unit tests in `pytest` validate Pydantic schema validation boundaries, dataset integrity, and metric aggregation formulas without making external network calls.

---

## Repository Structure

| File | Description |

| :--- | :--- |

| `schema.py` | Pydantic contracts defining `FlawType`, `FlawEvidence`, and `FramingEvaluationReport`. |

| `evaluator.py` | Live Gemini caller featuring exponential backoff and model cascade failover. |

| `dataset.py` | Curated benchmark cases (biased narratives and balanced negative controls). |

| `metrics.py` | Statistical aggregation of pass rates, severity distributions, and flaw frequencies. |

| `run_benchmark.py` | Batch execution script that runs the dataset and serializes run artifacts to JSON. |

| `test_*.py` | Hermetic unit tests covering schema bounds, metrics arithmetic, and dataset integrity. |

---

## Installation & Setup

### 1. Clone the Repository

```bash

git clone [https://github.com/berkertun/historiographical-framing-evaluator.git](https://github.com/berkertun/historiographical-framing-evaluator.git)

cd historiographical-framing-evaluator

```

### 2. Configure Virtual Environment

```bash

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

```

### 3. Set API Credentials

Create a `.env` file in the project root:

```bash

GEMINI_API_KEY="your-gemini-api-key-here"

```

---

## Running the Harness

### Run Batch Benchmark

Evaluates all cases in `dataset.py`, computes aggregate metrics, and exports `benchmark_results.json`:

```bash

python run_[benchmark.py](http://benchmark.py)

```

### Run Hermetic Unit Tests

Executes the offline test suite:

```bash

pytest -v

```

---

## Proof-of-Concept Benchmark (v0)

The initial validation dataset tests the evaluator across paired historical passages regarding 19th-century Ottoman administrative reforms, conceptual evolution (*hürriyet*), and legal codification (*Mecelle-i Ahkâm-ı Adliye*):

* **Biased Cases (3):** Narratives intentionally written with overt developmentalist tropes, passive reception narratives, and moral judgments.

* **Negative Controls (2):** Methodologically grounded narratives articulating institutional negotiation and Hanafi jurisprudence without trigger phrases.

```text

=== Benchmark Summary Metrics ===

Total Cases: 5

Passed Cases: 5

Accuracy: 100.0%

Total Flaws Identified: 8

Average Flaw Severity: 4.00/5.0

Flaw Breakdown by Type:

  - whig_teleology: 2

  - eurocentric_developmentalism: 3

  - agency_flattening: 3

```

### Current Scope & Methodological Limitations

* **Curated Exemplars:** The current 5-case benchmark functions as an architectural proof-of-concept to verify that the evaluator detects explicit framing distortions while avoiding false positives on control texts.

* **Future Work:** Benchmark v1 will expand beyond stylized caricatures to evaluate live, unprompted LLM responses on non-Western legal reforms, cross-referenced against multiple professional historian annotators.