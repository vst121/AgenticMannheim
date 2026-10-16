
class FakeJevClient:
    """Returns a deterministic assessment without calling an external API."""

    def assess_evidence(
        self,
        request_description: str,
        proposal_description: str,
        findings: list[dict[str, object]],
    ) -> tuple[str, float]:
        if not findings:
            return "insufficient", 0.95

        return "partially_sufficient", 0.85
