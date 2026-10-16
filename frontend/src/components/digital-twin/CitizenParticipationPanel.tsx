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

export function CitizenParticipationPanel({
  selectedLocation,
}: CitizenParticipationPanelProps) {
  const [requestType, setRequestType] =
    useState<CitizenRequestType>("safety_concern");
  const [description, setDescription] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
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
        `${env.apiBaseUrl}/api/citizen-participation/requests`,
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
          errorBody?.detail ??
            `Request submission failed (${response.status}).`,
        );
      }

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

  return (
    <section className="absolute right-4 top-4 z-10 w-80 max-w-[calc(100vw-2rem)] rounded-lg bg-white p-4 shadow-lg">
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
        disabled={isSubmitting}
        className="mt-4 w-full rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {isSubmitting ? "Submitting..." : "Submit request"}
      </button>

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
