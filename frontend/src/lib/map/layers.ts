import type {
  CircleLayerSpecification,
  LineLayerSpecification,
} from "maplibre-gl";

export const digitalTwinRoadLayer: LineLayerSpecification = {
  id: "digital-twin-roads",
  type: "line",
  source: "digital-twin-roads",
  paint: {
    "line-color": "#061e46",
    "line-width": 3,
    "line-opacity": 0.8,
  },
};

export const digitalTwinIntersectionLayer: CircleLayerSpecification = {
  id: "digital-twin-intersections",
  type: "circle",
  source: "digital-twin-intersections",
  paint: {
    "circle-radius": 4,
    "circle-opacity": 0.9,
    "circle-color": [
      "match",
      ["get", "traffic_light"],
      "red",
      "#ef4444",
      "yellow",
      "#facc15",
      "green",
      "#22c55e",
      "#6b7280",
    ],
    "circle-stroke-color": "#ffffff",
    "circle-stroke-width": 1,
  },
};

export const digitalTwinVehicleLayer: CircleLayerSpecification = {
  id: "digital-twin-vehicles",
  type: "circle",
  source: "digital-twin-vehicles",
  paint: {
    "circle-color": "#f80909",
    "circle-radius": 6,
    "circle-opacity": 1,
    "circle-stroke-width": 1,
  },
};

