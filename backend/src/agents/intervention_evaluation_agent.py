import json
from uuid import UUID

from domain.citizen_request import CitizenRequest
from domain.intervention_evaluation import (
    EvaluationFinding,
    EvaluationOutcome,
    InterventionEvaluation,
)
from domain.intervention_proposal import InterventionProposal
from domain.investigation import Investigation
from infrastructure.ai.openrouter_client import OpenRouterClient


class InterventionEvaluationAgent:
    def __init__(self, llm_client: OpenRouterClient) -> None:
        self._llm_client = llm_client

    def evaluate(
        self,
        request: CitizenRequest,
        proposal: InterventionProposal,
        investigation: Investigation,
    ) -> InterventionEvaluation:
        evidence = [
            {
                "category": finding.category,
                "description": finding.description,
                "source": finding.source,
                "confidence": finding.confidence,
            }
            for finding in investigation.findings
        ]

        system_prompt = """
You are an intervention evaluation agent for AgenticMannheim,
an experimental Digital Twin of Mannheim.

Evaluate a proposed intervention using only the supplied request,
proposal, and investigation evidence.

Rules:
- Treat investigation findings as evidence, not unquestionable truth.
- Do not invent facts, measurements, or simulation results.
- Distinguish observed evidence from assumptions and evidence gaps.
- Assess expected benefits, potential risks, and uncertainty.
- Do not issue traffic-light commands or modify Digital Twin state.
- Do not treat the intervention type as a traffic-light state.
- Return only valid JSON matching this schema:
{
  "outcome": "favorable | unfavorable | inconclusive",
  "summary": "concise explanation",
  "findings": [
    {
      "category": "evidence or concern category",
      "description": "reasoning grounded in supplied information",
      "source": "source reference or evaluation reasoning",
      "confidence": 0.0
    }
  ],
  "expected_benefits": ["benefit"],
  "potential_risks": ["risk"]
}

Use "inconclusive" when the available evidence is insufficient.
Confidence must be between 0 and 1.
""".strip()

        user_prompt = json.dumps(
            {
                "request": {
                    "id": str(request.id),
                    "type": request.request_type.value,
                    "description": request.description,
                    "location": {
                        "latitude": request.location.latitude,
                        "longitude": request.location.longitude,
                    },
                },
                "proposal": {
                    "id": str(proposal.id),
                    "type": proposal.intervention_type.value,
                    "title": proposal.title,
                    "description": proposal.description,
                    "expected_benefits": proposal.expected_benefits,
                    "potential_risks": proposal.potential_risks,
                },
                "investigation": {
                    "status": investigation.status.value,
                    "findings": evidence,
                },
            },
            ensure_ascii=False,
        )

        response = self._llm_client.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        try:
            result = json.loads(response)
            outcome = EvaluationOutcome(result["outcome"])
            summary = result["summary"]

            findings = [
                EvaluationFinding(
                    category=item["category"],
                    description=item["description"],
                    source=item["source"],
                    confidence=float(item["confidence"]),
                )
                for item in result["findings"]
            ]

            benefits = result["expected_benefits"]
            risks = result["potential_risks"]

            if not isinstance(summary, str) or not summary.strip():
                raise ValueError("Evaluation summary must not be empty.")

            if not isinstance(benefits, list) or not all(
                isinstance(item, str) for item in benefits
            ):
                raise ValueError("Expected benefits must be a list of strings.")

            if not isinstance(risks, list) or not all(
                isinstance(item, str) for item in risks
            ):
                raise ValueError("Potential risks must be a list of strings.")

        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            raise ValueError(
                "The LLM returned an invalid intervention evaluation."
            ) from exc

        return InterventionEvaluation(
            proposal_id=proposal.id,
            outcome=outcome,
            summary=summary.strip(),
            findings=findings,
            expected_benefits=benefits,
            potential_risks=risks,
            correlation_id=proposal.correlation_id,
        )
