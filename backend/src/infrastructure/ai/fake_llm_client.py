
import json


class FakeLLMClient:
    """Returns a deterministic intervention evaluation without an API call."""

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        request = json.loads(user_prompt)
        investigation = request.get("investigation", {})
        findings = investigation.get("findings", [])

        if findings:
            outcome = "favorable"
            summary = (
                "The investigation provides preliminary evidence "
                "supporting the proposed intervention."
            )
            evaluation_findings = [
                {
                    "category": "evidence_review",
                    "description": (
                        "The investigation contains findings relevant "
                        "to the citizen request."
                    ),
                    "source": "fake_llm",
                    "confidence": 0.85,
                }
            ]
        else:
            outcome = "inconclusive"
            summary = (
                "There is insufficient investigation evidence "
                "to assess the proposed intervention."
            )
            evaluation_findings = [
                {
                    "category": "evidence_gap",
                    "description": "No investigation findings were supplied.",
                    "source": "fake_llm",
                    "confidence": 0.95,
                }
            ]

        return json.dumps(
            {
                "outcome": outcome,
                "summary": summary,
                "findings": evaluation_findings,
                "expected_benefits": request["proposal"].get(
                    "expected_benefits", []
                ),
                "potential_risks": request["proposal"].get(
                    "potential_risks", []
                ),
            },
            ensure_ascii=False,
        )
