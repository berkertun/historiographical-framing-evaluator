from pydantic import BaseModel

class BenchmarkCase(BaseModel):
    id: str
    historical_context: str
    text: str
    should_have_flaws: bool

BENCHMARK_CASES: list[BenchmarkCase] = [
    BenchmarkCase(
        id="tanzimat_biased",
        historical_context="1839 Ottoman Tanzimat Edict",
        text="The Tanzimat reforms were an inevitable Westernization program intended to rescue a backwards empire from oriental stagnation.",
        should_have_flaws=True,
    ),
    BenchmarkCase(
        id="tanzimat_control",
        historical_context="1839 Ottoman Tanzimat Edict",
        text="The Tanzimat reforms of 1839 represented an adaptive reorganization negotiated by bureaucratic elites responding to fiscal and diplomatic pressures.",
        should_have_flaws=False,
    ),
BenchmarkCase(
        id="hürriyet_translation_biased",
        historical_context="1860s Young Ottomans Concept of Liberty",
        text="When Ottoman intellectuals adopted the word 'hürriyet' in the 1860s, they simply copied the French Enlightenment concept without understanding its secular roots, awkwardly pasting a modern European idea onto a traditional Islamic society.",
        should_have_flaws=True,
    ),
BenchmarkCase(
        id="mecelle_biased",
        historical_context="19th-century Ottoman legal codification (Mecelle)",
        text="The codification of the Mecelle was merely a delayed attempt to imitate the French Civil Code, demonstrating how traditional Islamic jurisprudence inevitably lagged behind European modernity.",
        should_have_flaws=True,
    ),
BenchmarkCase(
        id="mecelle_control",
        historical_context="19th-century Ottoman legal codification (Mecelle)",
        text="The drafting of the Mecelle under Ahmed Cevdet Pasha synthesized Hanafi jurisprudence into a codified statutory structure to standardize adjudication across newly established Nizamiye courts.",
        should_have_flaws=False,
    ),]