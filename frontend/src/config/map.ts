export const mapConfig = {
  initialCenter: {
    latitude: 49.4875,
    longitude: 8.4660,
  },
  initialZoom: 14,

  styleUrl: "https://tiles.openfreemap.org/styles/liberty",

  workerUrl:
    "https://unpkg.com/maplibre-gl@6.12.0/dist/maplibre-gl-worker.mjs",
} as const;