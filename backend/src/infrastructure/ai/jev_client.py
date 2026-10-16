from typesafe_sdk import Choice, TypeSafeClient

from infrastructure.config.settings import settings


class JevClient:
    """Provides bounded judgments using Jev."""

    def __init__(self) -> None:
        if not settings.typesafe_api_key:
            raise ValueError("TYPESAFE_API_KEY is not configured.")

        self._client = TypeSafeClient(
            api_key=settings.typesafe_api_key,
            base_url=settings.jev_base_url,
            model=settings.jev_model,
        )

    def assess_evidence(
        self,
        request_description: str,
        proposal_description: str,
        findings: list[dict[str, object]],
    ) -> tuple[str, float]:
        response = self._client.system_one(
            state={
                "citizen_request": request_description,
                "proposed_intervention": proposal_description,
                "investigation_findings": findings,
            },
            questions={
                "evidence_assessment": Choice(
                    instructions=(
                        "Assess how well the supplied investigation findings "
                        "support proceeding with the proposed intervention. "
                        "Consider relevance, reliability, and evidence gaps. "
                        "Do not assume facts that are not provided."
                    ),
                    criteria={
                        "sufficient": (
                            "The available evidence provides a reasonable "
                            "basis to proceed to further evaluation."
                        ),
                        "partially_sufficient": (
                            "Some relevant evidence exists, but important "
                            "questions remain unresolved."
                        ),
                        "insufficient": (
                            "The available evidence does not adequately "
                            "support proceeding with the proposal."
                        ),
                    },
                ),
            },
        )

        answer = response.choices["evidence_assessment"]
        return answer.choice, answer.confidence
