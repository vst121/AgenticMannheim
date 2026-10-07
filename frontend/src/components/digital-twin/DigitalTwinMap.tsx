"use client";

import { useEffect, useRef } from "react";
import * as maplibregl from "maplibre-gl";

import { env } from "@/config/env";
import { mapConfig } from "@/config/map";

import "maplibre-gl/dist/maplibre-gl.css";

maplibregl.setWorkerUrl(mapConfig.workerUrl);

/**
 * Sanitizes shield filters in style layers to prevent worker type warnings.
 * Replaces direct ["get", "prop"] lookups with safe fallbacks ["coalesce", ["get", "prop"], 0].
 */
function sanitizeStyleFilters(
  style: maplibregl.StyleSpecification,
): maplibregl.StyleSpecification {
  if (!style.layers) return style;

  const sanitizeExpr = (expr: any): any => {
    if (!Array.isArray(expr)) return expr;
    return expr.map((arg) => {
      if (Array.isArray(arg)) {
        if (arg[0] === "get" && typeof arg[1] === "string") {
          return ["coalesce", arg, 0];
        }
        return sanitizeExpr(arg);
      }
      return arg;
    });
  };

  const cleanLayers = style.layers.map((layer) => {
    if (
      layer.filter &&
      (layer.id.includes("shield") || layer.id.includes("highway"))
    ) {
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

    // Intercept console noise on main thread
    const originalWarn = console.warn;
    const originalError = console.error;

    const filterMapLibreNoise = (args: unknown[]) => {
      const msg = args.map(String).join(" ");
      return (
        msg.includes("Expected value to be of type number") ||
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

        // Load style JSON and clean layer filters before map initialization
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

        // Initialize MapLibre
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

        // Resolve missing sprite icons with transparent 1x1 fallback
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

        // Load GeoJSON layer once map style finishes loading
        map.on("load", async () => {
          try {
            const response = await fetch(`${env.apiBaseUrl}/api/roads/geojson`);

            if (!response.ok) {
              throw new Error(
                `Failed to load road network: ${response.status}`,
              );
            }

            const roadGeoJson =
              (await response.json()) as GeoJSON.FeatureCollection;

            if (!map.getSource("digital-twin-roads")) {
              map.addSource("digital-twin-roads", {
                type: "geojson",
                data: roadGeoJson,
              });

              map.addLayer({
                id: "digital-twin-roads",
                type: "line",
                source: "digital-twin-roads",
                paint: {
                  "line-color": "#061e46",
                  "line-width": 3,
                  "line-opacity": 0.8,
                },
              });
            }
          } catch (error) {
            originalError("Error loading road GeoJSON:", error);
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
