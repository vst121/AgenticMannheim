"use client";

import { useState } from "react";

const BACKEND_BASE_URL =
  process.env.NEXT_PUBLIC_BACKEND_BASE_URL ?? "http://localhost:8000";

export function TrafficControlPanel() {
  const [isCreatingEmergency, setIsCreatingEmergency] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const createEmergency = async () => {
    setIsCreatingEmergency(true);
    setMessage(null);

    try {
      const response = await fetch(
        `${BACKEND_BASE_URL}/api/scenarios/emergency`,
        {
          method: "POST",
        },
      );

      if (!response.ok) {
        throw new Error("Failed to create emergency scenario.");
      }

      const scenario = await response.json();

      setMessage(`Emergency vehicle ${scenario.vehicle_id} created.`);
    } catch (error) {
      console.error("Failed to create emergency scenario:", error);
      setMessage("Failed to create emergency scenario.");
    } finally {
      setIsCreatingEmergency(false);
    }
  };

  return (
    <section className="absolute left-4 top-4 z-10 w-64 rounded-lg bg-white p-4 shadow-lg">
      <h2 className="text-lg font-semibold text-gray-900">Traffic Control</h2>

      <div className="mt-4">
        <h3 className="text-sm font-medium text-gray-600">Scenarios</h3>

        <button
          type="button"
          onClick={createEmergency}
          disabled={isCreatingEmergency}
          className="mt-2 w-full rounded-md bg-red-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-red-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {isCreatingEmergency ? "Creating..." : "Create Emergency"}
        </button>
      </div>

      {message && (
        <p className="mt-3 break-words text-xs text-gray-600">{message}</p>
      )}
    </section>
  );
}
