from enum import Enum
from pydantic import BaseModel, Field

class FlawType(str, Enum):
    WHIG_TELEOLOGY = "whig_teleology"
    EUROCENTRIC_DEVELOPMENTALISM = "eurocentric_developmentalism"
    ANACHRONISTIC_MORALISM = "anachronistic_moralism"
    AGENCY_FLATTENING = "agency_flattening"

class FlawEvidence(BaseModel):
    flaw_type: FlawType = Field(
        description="The category of historiographical or teleological bias detected."
    )
    quote: str = Field(
        description="The exact verbatim excerpt demonstrating the framing flaw."
    )
    explanation: str = Field(
        description="Scholarly critique explaining why this reflects historiographical bias."
    )
class FramingEvaluationReport(BaseModel):
    has_framing_flaws: bool = Field(
        description="True if any teleological, eurocentric, or moralistic framing flaws exist."
    )
    detected_flaws: list[FlawEvidence] = Field(
        default_factory=list,
        description="A list of specific historiographical flaws identified with quotes and critiques."
    )
    overall_assessment: str = Field(
        description="A scholarly synthesis evaluating the text's historical contextualization."
    )