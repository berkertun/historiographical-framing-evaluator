from enum import Enum
from pydantic import BaseModel, Field

class FlawType(str, Enum):
    WHIG_TELEOLOGY = "whig_teleology"
    EUROCENTRIC_DEVELOPMENTALISM = "eurocentric_developmentalism"
    ANACHRONISTIC_MORALISM = "anachronistic_moralism"
    AGENCY_FLATTENING = "agency_flattening"

class FlawEvidence(BaseModel):
    flaw_type: FlawType
    quote: str
    explanation: str
    severity: int = Field(
        ...,
        ge=1,
        le=5,
        description="Severity score from 1 (subtle implicit bias) to 5 (overt deterministic distortion)."
    )

class FramingEvaluationReport(BaseModel):
    has_framing_flaws: bool
    detected_flaws: list[FlawEvidence]
    overall_assessment: str