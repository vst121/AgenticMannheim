import { DigitalTwinMap } from "@/components/digital-twin/DigitalTwinMap";
import { TrafficControlPanel } from "@/components/digital-twin/TrafficControlPanel";

export default function Home() {
  return (
    <main className="relative h-screen w-screen">
      <DigitalTwinMap />

      <TrafficControlPanel />
    </main>
  );
}
