"use client";

import { useEffect, useRef } from "react";
import * as maplibregl from "maplibre-gl";

import { env } from "@/config/env";
import { mapConfig } from "@/config/map";

import "maplibre-gl/dist/maplibre-gl.css";

import {
  digitalTwinIntersectionLayer,
  digitalTwinRoadLayer,
  digitalTwinVehicleLayer,
} from "@/lib/map/layers";

import {
  digitalTwinIntersectionSource,
  digitalTwinRoadSource,
  digitalTwinVehicleSource,
} from "@/lib/map/sources";

maplibregl.setWorkerUrl(mapConfig.workerUrl);

function sanitizeStyleFilters(
  style: maplibregl.StyleSpecification,
): maplibregl.StyleSpecification {
  if (!style.layers) return style;

  const sanitizeExpr = (expr: any): any => {
    if (!Array.isArray(expr)) return expr;

    if (expr[0] === "get" && typeof expr[1] === "string") {
      return ["coalesce", expr, 0];
    }

    return expr.map((arg) => (Array.isArray(arg) ? sanitizeExpr(arg) : arg));
  };

  const cleanLayers = style.layers.map((layer) => {
    if (layer.filter) {
      return { ...layer, filter: sanitizeExpr(layer.filter) };
    }
    return layer;
  });

  return { ...style, layers: cleanLayers };
}

export function DigitalTwinMap() {
  const mapContainerRef = useRef<HTMLDivElement | null>(null);
  const mapRef = useRef<maplibregl.Map | null>(null);

  useEffect(() => {
    if (!mapContainerRef.current || mapRef.current) {
      return;
    }

    let isMounted = true;

    const originalWarn = console.warn;
    const originalError = console.error;

    const filterMapLibreNoise = (args: unknown[]) => {
      const msg = args
        .map((a) => (typeof a === "object" ? JSON.stringify(a) : String(a)))
        .join(" ");
      return (
        msg.includes("Expected value to be of type number") ||
        msg.includes("found null instead") ||
        msg.includes("highway-shield") ||
        msg.includes("could not be loaded")
      );
    };

    console.warn = (...args: unknown[]) => {
      if (filterMapLibreNoise(args)) return;
      originalWarn.apply(console, args);
    };

    console.error = (...args: unknown[]) => {
      if (filterMapLibreNoise(args)) return;
      originalError.apply(console, args);
    };

    async function initMap() {
      try {
        let styleInput: maplibregl.StyleSpecification | string =
          mapConfig.styleUrl;

        if (
          typeof mapConfig.styleUrl === "string" &&
          mapConfig.styleUrl.startsWith("http")
        ) {
          const res = await fetch(mapConfig.styleUrl);
          if (res.ok) {
            const rawStyle =
              (await res.json()) as maplibregl.StyleSpecification;
            styleInput = sanitizeStyleFilters(rawStyle);
          }
        }

        if (!isMounted || !mapContainerRef.current) return;

        const map = new maplibregl.Map({
          container: mapContainerRef.current,
          style: styleInput,
          center: [
            mapConfig.initialCenter.longitude,
            mapConfig.initialCenter.latitude,
          ],
          zoom: mapConfig.initialZoom,
          localIdeographFontFamily: "sans-serif",
        });

        map.on("error", (e) => {
          if (
            e?.error?.message?.includes("Expected value to be of type number")
          ) {
            return;
          }
        });

        map.setMissingStyleImageResolver(() => {
          const canvas = document.createElement("canvas");
          canvas.width = 1;
          canvas.height = 1;
          const ctx = canvas.getContext("2d");
          if (ctx) ctx.clearRect(0, 0, 1, 1);
          return {
            width: 1,
            height: 1,
            data: ctx?.getImageData(0, 0, 1, 1).data || new Uint8Array(4),
          };
        });

        mapRef.current = map;

        map.on("load", async () => {
          try {
            const trafficLightImages = [
              ["traffic-light-red", "/icons/traffic-light-red.png"],
              ["traffic-light-yellow", "/icons/traffic-light-yellow.png"],
              ["traffic-light-green", "/icons/traffic-light-green.png"],
            ] as const;

            for (const [imageId, imagePath] of trafficLightImages) {
              if (!map.hasImage(imageId)) {
                const image = await map.loadImage(imagePath);
                map.addImage(imageId, image.data);
              }
            }

            if (!map.getSource("digital-twin-roads")) {
              map.addSource("digital-twin-roads", digitalTwinRoadSource);
            }

            if (!map.getSource("digital-twin-intersections")) {
              map.addSource(
                "digital-twin-intersections",
                digitalTwinIntersectionSource,
              );
            }

            if (!map.getSource("digital-twin-vehicles")) {
              map.addSource("digital-twin-vehicles", digitalTwinVehicleSource);
            }

            if (!map.getLayer("digital-twin-roads")) {
              map.addLayer(digitalTwinRoadLayer);
            }

            if (!map.getLayer("digital-twin-intersections")) {
              map.addLayer(digitalTwinIntersectionLayer);
            }

            if (!map.getLayer("digital-twin-vehicles")) {
              map.addLayer(digitalTwinVehicleLayer);
            }

            const roadResponse = await fetch(
              `${env.apiBaseUrl}/api/roads/geojson`,
            );

            if (!roadResponse.ok) {
              throw new Error(
                `Failed to load road network: ${roadResponse.status}`,
              );
            }

            const roadGeoJson =
              (await roadResponse.json()) as GeoJSON.FeatureCollection;

            const roadSource = map.getSource(
              "digital-twin-roads",
            ) as maplibregl.GeoJSONSource;

            roadSource.setData(roadGeoJson);

            const intersectionResponse = await fetch(
              `${env.apiBaseUrl}/api/intersections/geojson`,
            );

            if (!intersectionResponse.ok) {
              throw new Error(
                `Failed to load intersections: ${intersectionResponse.status}`,
              );
            }

            const intersectionGeoJson =
              (await intersectionResponse.json()) as GeoJSON.FeatureCollection;

            const intersectionSource = map.getSource(
              "digital-twin-intersections",
            ) as maplibregl.GeoJSONSource;

            intersectionSource.setData(intersectionGeoJson);

            const vehicleResponse = await fetch(
              `${env.apiBaseUrl}/api/vehicles/geojson`,
            );

            if (!vehicleResponse.ok) {
              throw new Error(
                `Failed to load vehicles: ${vehicleResponse.status}`,
              );
            }

            const vehicleGeoJson =
              (await vehicleResponse.json()) as GeoJSON.FeatureCollection;

            const vehicleSource = map.getSource(
              "digital-twin-vehicles",
            ) as maplibregl.GeoJSONSource;

            vehicleSource.setData(vehicleGeoJson);
          } catch (error) {
            originalError("Error loading Digital Twin GeoJSON:", error);
          }
        });
      } catch (err) {
        originalError("Error setting up MapLibre instance:", err);
      }
    }

    initMap();

    return () => {
      isMounted = false;
      console.warn = originalWarn;
      console.error = originalError;
      if (mapRef.current) {
        mapRef.current.remove();
        mapRef.current = null;
      }
    };
  }, []);

  return <div ref={mapContainerRef} className="h-full w-full" />;
}
