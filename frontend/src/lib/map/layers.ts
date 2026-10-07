import type {
  CircleLayerSpecification,
  LineLayerSpecification,
  SymbolLayerSpecification,
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

export const digitalTwinIntersectionLayer: SymbolLayerSpecification = {
  id: "digital-twin-intersections",
  type: "symbol",
  source: "digital-twin-intersections",
  filter: [
    "!=",
    ["get", "traffic_light"],
    null,
  ],
  layout: {
    "icon-image": [
      "match",
      ["get", "traffic_light"],
      "red",
      "traffic-light-red",
      "yellow",
      "traffic-light-yellow",
      "green",
      "traffic-light-green",
      "traffic-light-red",
    ],
    "icon-size": 0.12,
    "icon-allow-overlap": true,
    "icon-ignore-placement": true,
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

