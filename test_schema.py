import pytest
from pydantic import ValidationError
from schema import FlawEvidence, FlawType


def test_flaw_evidence_severity_bounds():
    with pytest.raises(ValidationError):
        FlawEvidence(
            flaw_type=FlawType.WHIG_TELEOLOGY,
            severity=6,
            quote="inevitable march of progress",
            explanation="Exceeds maximum score of 5.",
        )

def test_flaw_evidence_lower_severity_bound():
    with pytest.raises(ValidationError):
        FlawEvidence(
            flaw_type=FlawType.ANACHRONISTIC_MORALISM,
            severity=0,
            quote="backward institutions",
            explanation="Below minimum score of 1.",
        )


def test_flaw_evidence_valid_instance():
    flaw = FlawEvidence(
        flaw_type=FlawType.AGENCY_FLATTENING,
        severity=3,
        quote="passive recipients of modern law",
        explanation="Erases local strategic negotiation.",
    )
    assert flaw.severity == 3
    assert flaw.flaw_type == FlawType.AGENCY_FLATTENING