
"use client";

import { useState } from "react";
import { env } from "@/config/env";

type SelectedLocation = {
  latitude: number;
  longitude: number;
};

type CitizenParticipationPanelProps = {
  selectedLocation: SelectedLocation | null;
};

type CitizenRequestType =
  | "incident"
  | "safety_concern"
  | "suggestion"
  | "general_request";

type CitizenRequestResponse = {
  id: string;
  request_type: CitizenRequestType;
  description: string;
  latitude: number;
  longitude: number;
  status: string;
  created_at: string;
  correlation_id: string;
};

type InvestigationFinding = {
  category: string;
  description: string;
  source: string;
  confidence: number;
};

type InvestigationResponse = {
  id: string;
  request_id: string;
  status: string;
  findings: InvestigationFinding[];
  related_request_ids: string[];
  related_event_ids: string[];
  correlation_id: string;
};

type InterventionProposal = {
  id: string;
  request_id: string;
  investigation_id: string;
  intervention_type: string;
  title: string;
  description: string;
  target_intersection_id: string | null;
  expected_benefits: string[];
  potential_risks: string[];
  status: string;
  correlation_id: string;
};

type EvaluationFinding = {
  category: string;
  description: string;
  source: string;
  confidence: number;
};

type InterventionEvaluation = {
  id: string;
  proposal_id: string;
  outcome: "favorable" | "unfavorable" | "inconclusive" | string;
  summary: string;
  findings: EvaluationFinding[];
  expected_benefits: string[];
  potential_risks: string[];
  created_at: string;
  correlation_id: string;
};

export function CitizenParticipationPanel({
  selectedLocation,
}: CitizenParticipationPanelProps) {
  const [requestType, setRequestType] =
    useState<CitizenRequestType>("safety_concern");
  const [description, setDescription] = useState("");

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isInvestigating, setIsInvestigating] = useState(false);
  const [isGeneratingProposal, setIsGeneratingProposal] = useState(false);
  const [isEvaluating, setIsEvaluating] = useState(false);

  const [submittedRequest, setSubmittedRequest] =
    useState<CitizenRequestResponse | null>(null);
  const [investigation, setInvestigation] =
    useState<InvestigationResponse | null>(null);
  const [proposal, setProposal] =
    useState<InterventionProposal | null>(null);
  const [evaluation, setEvaluation] =
    useState<InterventionEvaluation | null>(null);

  const [message, setMessage] = useState<string | null>(null);
  const [isError, setIsError] = useState(false);

  const submitRequest = async () => {
    if (!selectedLocation) {
      setMessage("Click the map to select a location first.");
      setIsError(true);
      return;
    }

    if (!description.trim()) {
      setMessage("Please describe your request.");
      setIsError(true);
      return;
    }

    setIsSubmitting(true);
    setMessage(null);
    setIsError(false);

    try {
      const response = await fetch(
        `${env.apiBaseUrl}/api/citizen-requests`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            request_type: requestType,
            description: description.trim(),
            latitude: selectedLocation.latitude,
            longitude: selectedLocation.longitude,
          }),
        },
      );

      if (!response.ok) {
        const errorBody = await response.json().catch(() => null);
        throw new Error(
          typeof errorBody?.detail === "string"
            ? errorBody.detail
            : `Request submission failed (${response.status}).`,
        );
      }

      const createdRequest =
        (await response.json()) as CitizenRequestResponse;

      setSubmittedRequest(createdRequest);
      setInvestigation(null);
      setProposal(null);
      setEvaluation(null);
      setDescription("");
      setMessage("Your request was submitted successfully.");
    } catch (error) {
      setIsError(true);
      setMessage(
        error instanceof Error
          ? error.message
          : "Failed to submit your request.",
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  const investigateRequest = async () => {
    if (!submittedRequest) return;

    setIsInvestigating(true);
    setMessage(null);
    setIsError(false);
    setInvestigation(null);
    setProposal(null);
    setEvaluation(null);

    try {
      const response = await fetch(
        `${env.apiBaseUrl}/api/citizen-requests/${submittedRequest.id}/investigation`,
      );

      if (!response.ok) {
        const errorBody = await response.json().catch(() => null);
        throw new Error(
          typeof errorBody?.detail === "string"
            ? errorBody.detail
            : `Investigation failed (${response.status}).`,
        );
      }

      const result =
        (await response.json()) as InvestigationResponse;

      setInvestigation(result);
      setMessage("Investigation results received.");
    } catch (error) {
      setIsError(true);
      setMessage(
        error instanceof Error
          ? error.message
          : "Failed to investigate your request.",
      );
    } finally {
      setIsInvestigating(false);
    }
  };

  const generateProposal = async () => {
    if (!submittedRequest || !investigation) return;

    setIsGeneratingProposal(true);
    setMessage(null);
    setIsError(false);
    setProposal(null);
    setEvaluation(null);

    try {
      const response = await fetch(
        `${env.apiBaseUrl}/api/citizen-requests/${submittedRequest.id}/proposal`,
        {
          method: "POST",
        },
      );

      if (!response.ok) {
        const errorBody = await response.json().catch(() => null);
        throw new Error(
          typeof errorBody?.detail === "string"
            ? errorBody.detail
            : `Proposal generation failed (${response.status}).`,
        );
      }

      const generatedProposal =
        (await response.json()) as InterventionProposal;

      setProposal(generatedProposal);
      setMessage("Intervention proposal generated successfully.");
    } catch (error) {
      setIsError(true);
      setMessage(
        error instanceof Error
          ? error.message
          : "Failed to generate an intervention proposal.",
      );
    } finally {
      setIsGeneratingProposal(false);
    }
  };

  const evaluateProposal = async () => {
    if (!proposal) return;

    setIsEvaluating(true);
    setMessage(null);
    setIsError(false);
    setEvaluation(null);

    try {
      const response = await fetch(
        `${env.apiBaseUrl}/api/citizen-requests/proposals/${proposal.id}/evaluations`,
        {
          method: "POST",
        },
      );

      if (!response.ok) {
        const errorBody = await response.json().catch(() => null);
        throw new Error(
          typeof errorBody?.detail === "string"
            ? errorBody.detail
            : `Evaluation failed (${response.status}).`,
        );
      }

      const result =
        (await response.json()) as InterventionEvaluation;

      setEvaluation(result);
      setMessage("Intervention evaluation completed.");
    } catch (error) {
      setIsError(true);
      setMessage(
        error instanceof Error
          ? error.message
          : "Failed to evaluate the intervention.",
      );
    } finally {
      setIsEvaluating(false);
    }
  };

  return (
    <section className="absolute right-4 top-4 z-10 max-h-[calc(100vh-2rem)] w-80 max-w-[calc(100vw-2rem)] overflow-y-auto rounded-lg bg-white p-4 shadow-lg">
      <h2 className="text-lg font-semibold text-gray-900">
        Citizen Participation
      </h2>

      <p className="mt-1 text-sm text-gray-600">
        Report an issue or suggest an improvement for Mannheim.
      </p>

      <div className="mt-4">
        <label
          htmlFor="citizen-request-type"
          className="mb-1 block text-sm font-medium text-gray-700"
        >
          Request type
        </label>

        <select
          id="citizen-request-type"
          value={requestType}
          onChange={(event) =>
            setRequestType(event.target.value as CitizenRequestType)
          }
          className="w-full rounded-md border border-gray-300 p-2 text-sm text-gray-900"
        >
          <option value="incident">Incident</option>
          <option value="safety_concern">Safety concern</option>
          <option value="suggestion">Suggestion</option>
          <option value="general_request">General request</option>
        </select>
      </div>

      <div className="mt-3">
        <label
          htmlFor="citizen-request-description"
          className="mb-1 block text-sm font-medium text-gray-700"
        >
          Description
        </label>

        <textarea
          id="citizen-request-description"
          value={description}
          onChange={(event) => setDescription(event.target.value)}
          placeholder="Describe the issue or improvement..."
          rows={4}
          maxLength={2000}
          className="w-full resize-y rounded-md border border-gray-300 p-2 text-sm text-gray-900 placeholder:text-gray-400"
        />
      </div>

      <div className="mt-3 rounded-md bg-gray-50 p-3 text-sm text-gray-700">
        <p className="font-medium">Selected map location</p>

        {selectedLocation ? (
          <div className="mt-1 space-y-1">
            <p>Latitude: {selectedLocation.latitude.toFixed(6)}</p>
            <p>Longitude: {selectedLocation.longitude.toFixed(6)}</p>
          </div>
        ) : (
          <p className="mt-1 text-gray-500">
            Click anywhere on the map to select a location.
          </p>
        )}
      </div>

      <button
        type="button"
        onClick={submitRequest}
        disabled={
          isSubmitting ||
          isInvestigating ||
          isGeneratingProposal ||
          isEvaluating
        }
        className="mt-4 w-full rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {isSubmitting ? "Submitting..." : "Submit request"}
      </button>

      {submittedRequest && (
        <div className="mt-4 rounded-md border border-gray-200 p-3">
          <h3 className="text-sm font-semibold text-gray-900">
            Submitted request
          </h3>

          <p className="mt-2 text-xs text-gray-500">Request ID</p>
          <p className="break-all text-xs text-gray-800">
            {submittedRequest.id}
          </p>

          <p className="mt-2 text-sm text-gray-700">
            Status:{" "}
            <span className="font-medium">{submittedRequest.status}</span>
          </p>

          <button
            type="button"
            onClick={investigateRequest}
            disabled={
              isInvestigating ||
              isSubmitting ||
              isGeneratingProposal ||
              isEvaluating
            }
            className="mt-3 w-full rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {isInvestigating ? "Investigating..." : "Investigate request"}
          </button>
        </div>
      )}

      {investigation && (
        <div className="mt-4 rounded-md border border-indigo-200 bg-indigo-50 p-3">
          <h3 className="text-sm font-semibold text-gray-900">
            Investigation results
          </h3>

          <p className="mt-2 text-sm text-gray-700">
            Status:{" "}
            <span className="font-medium">{investigation.status}</span>
          </p>

          <p className="mt-1 text-sm text-gray-700">
            Related requests: {investigation.related_request_ids.length}
          </p>

          <p className="text-sm text-gray-700">
            Related events: {investigation.related_event_ids.length}
          </p>

          <div className="mt-3">
            <h4 className="text-sm font-medium text-gray-900">
              Findings ({investigation.findings.length})
            </h4>

            {investigation.findings.length > 0 ? (
              <ul className="mt-2 space-y-3">
                {investigation.findings.map((finding, index) => (
                  <li
                    key={`${finding.category}-${finding.source}-${index}`}
                    className="rounded-md bg-white p-3"
                  >
                    <p className="text-sm font-medium capitalize text-gray-900">
                      {finding.category.replaceAll("_", " ")}
                    </p>

                    <p className="mt-1 text-sm text-gray-700">
                      {finding.description}
                    </p>

                    <p className="mt-2 text-xs text-gray-500">
                      Source: {finding.source}
                    </p>

                    <p className="text-xs text-gray-500">
                      Confidence: {(finding.confidence * 100).toFixed(0)}%
                    </p>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="mt-2 text-sm text-gray-600">
                No findings were returned for this investigation.
              </p>
            )}
          </div>

          <button
            type="button"
            onClick={generateProposal}
            disabled={
              isGeneratingProposal ||
              isInvestigating ||
              isSubmitting ||
              isEvaluating
            }
            className="mt-4 w-full rounded-md bg-purple-600 px-4 py-2 text-sm font-medium text-white hover:bg-purple-700 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {isGeneratingProposal
              ? "Generating proposal..."
              : "Generate intervention proposal"}
          </button>
        </div>
      )}

      {proposal && (
        <div className="mt-4 rounded-md border border-purple-200 bg-purple-50 p-3">
          <h3 className="text-sm font-semibold text-gray-900">
            Intervention proposal
          </h3>

          <p className="mt-2 text-xs font-medium uppercase tracking-wide text-purple-800">
            {proposal.intervention_type.replaceAll("_", " ")}
          </p>

          <h4 className="mt-1 text-base font-semibold text-gray-900">
            {proposal.title}
          </h4>

          <p className="mt-2 text-sm text-gray-700">
            {proposal.description}
          </p>

          <p className="mt-3 text-sm text-gray-700">
            Status:{" "}
            <span className="font-medium">{proposal.status}</span>
          </p>

          {proposal.expected_benefits.length > 0 && (
            <div className="mt-3">
              <h4 className="text-sm font-medium text-gray-900">
                Expected benefits
              </h4>
              <ul className="mt-1 list-disc space-y-1 pl-5 text-sm text-gray-700">
                {proposal.expected_benefits.map((benefit, index) => (
                  <li key={`${benefit}-${index}`}>{benefit}</li>
                ))}
              </ul>
            </div>
          )}

          {proposal.potential_risks.length > 0 && (
            <div className="mt-3">
              <h4 className="text-sm font-medium text-gray-900">
                Potential risks
              </h4>
              <ul className="mt-1 list-disc space-y-1 pl-5 text-sm text-gray-700">
                {proposal.potential_risks.map((risk, index) => (
                  <li key={`${risk}-${index}`}>{risk}</li>
                ))}
              </ul>
            </div>
          )}

          <p className="mt-3 break-all text-xs text-gray-500">
            Proposal ID: {proposal.id}
          </p>

          {proposal.target_intersection_id && (
            <p className="mt-1 break-all text-xs text-gray-500">
              Target intersection ID: {proposal.target_intersection_id}
            </p>
          )}

          <button
            type="button"
            onClick={evaluateProposal}
            disabled={
              isEvaluating ||
              isGeneratingProposal ||
              isInvestigating ||
              isSubmitting
            }
            className="mt-4 w-full rounded-md bg-teal-700 px-4 py-2 text-sm font-medium text-white hover:bg-teal-800 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {isEvaluating ? "Evaluating..." : "Evaluate intervention"}
          </button>
        </div>
      )}

      {evaluation && (
        <div className="mt-4 rounded-md border border-teal-200 bg-teal-50 p-3">
          <h3 className="text-sm font-semibold text-gray-900">
            Intervention evaluation
          </h3>

          <p className="mt-2 text-sm text-gray-700">
            Outcome:{" "}
            <span className="font-semibold capitalize">
              {evaluation.outcome.replaceAll("_", " ")}
            </span>
          </p>

          <p className="mt-2 text-sm text-gray-700">
            {evaluation.summary}
          </p>

          <div className="mt-3">
            <h4 className="text-sm font-medium text-gray-900">
              Evaluation findings ({evaluation.findings.length})
            </h4>

            {evaluation.findings.length > 0 ? (
              <ul className="mt-2 space-y-3">
                {evaluation.findings.map((finding, index) => (
                  <li
                    key={`${finding.category}-${finding.source}-${index}`}
                    className="rounded-md bg-white p-3"
                  >
                    <p className="text-sm font-medium capitalize text-gray-900">
                      {finding.category.replaceAll("_", " ")}
                    </p>

                    <p className="mt-1 text-sm text-gray-700">
                      {finding.description}
                    </p>

                    <p className="mt-2 text-xs text-gray-500">
                      Source: {finding.source}
                    </p>

                    <p className="text-xs text-gray-500">
                      Confidence: {(finding.confidence * 100).toFixed(0)}%
                    </p>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="mt-1 text-sm text-gray-600">
                No evaluation findings were returned.
              </p>
            )}
          </div>

          {evaluation.expected_benefits.length > 0 && (
            <div className="mt-3">
              <h4 className="text-sm font-medium text-gray-900">
                Expected benefits
              </h4>
              <ul className="mt-1 list-disc space-y-1 pl-5 text-sm text-gray-700">
                {evaluation.expected_benefits.map((benefit, index) => (
                  <li key={`${benefit}-${index}`}>{benefit}</li>
                ))}
              </ul>
            </div>
          )}

          {evaluation.potential_risks.length > 0 && (
            <div className="mt-3">
              <h4 className="text-sm font-medium text-gray-900">
                Potential risks
              </h4>
              <ul className="mt-1 list-disc space-y-1 pl-5 text-sm text-gray-700">
                {evaluation.potential_risks.map((risk, index) => (
                  <li key={`${risk}-${index}`}>{risk}</li>
                ))}
              </ul>
            </div>
          )}

          <p className="mt-3 break-all text-xs text-gray-500">
            Evaluation ID: {evaluation.id}
          </p>
        </div>
      )}

      {message && (
        <p
          role="status"
          aria-live="polite"
          className={`mt-3 text-sm ${
            isError ? "text-red-600" : "text-green-700"
          }`}
        >
          {message}
        </p>
      )}
    </section>
  );
}
