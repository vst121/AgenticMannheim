"use client";

import { useEffect, useRef } from "react";
import * as maplibregl from "maplibre-gl";

import { env } from "@/config/env";
import { mapConfig } from "@/config/map";

import "maplibre-gl/dist/maplibre-gl.css";

maplibregl.setWorkerUrl(mapConfig.workerUrl);

export function DigitalTwinMap() {
  const mapContainerRef = useRef<HTMLDivElement | null>(null);
  const mapRef = useRef<maplibregl.Map | null>(null);

  useEffect(() => {
    if (!mapContainerRef.current || mapRef.current) {
      return;
    }

    const map = new maplibregl.Map({
      container: mapContainerRef.current,
      style: mapConfig.styleUrl,
      center: [
        mapConfig.initialCenter.longitude,
        mapConfig.initialCenter.latitude,
      ],
      zoom: mapConfig.initialZoom,
    });

    map.on("styleimagemissing", (e) => {
      const id = e.id;
      if (!map.hasImage(id)) {
        map.addImage(id, {
          width: 1,
          height: 1,
          data: new Uint8Array([0, 0, 0, 0]),
        });
      }
    });

    mapRef.current = map;

    return () => {
      map.remove();
      mapRef.current = null;
    };
  }, []);

  return <div ref={mapContainerRef} className="h-full w-full" />;
}
