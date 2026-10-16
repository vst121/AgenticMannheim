"use client";

import { useState } from "react";

import { DigitalTwinMap } from "@/components/digital-twin/DigitalTwinMap";
import { TrafficControlPanel } from "@/components/digital-twin/TrafficControlPanel";
import { CitizenParticipationPanel } from "@/components/digital-twin/CitizenParticipationPanel";

type SelectedLocation = {
  latitude: number;
  longitude: number;
};

export default function Home() {
  const [selectedLocation, setSelectedLocation] =
    useState<SelectedLocation | null>(null);

  return (
    <main className="relative h-screen w-screen">
      <DigitalTwinMap onLocationSelect={setSelectedLocation} />

      <TrafficControlPanel />

      <CitizenParticipationPanel selectedLocation={selectedLocation} />
    </main>
  );
}
