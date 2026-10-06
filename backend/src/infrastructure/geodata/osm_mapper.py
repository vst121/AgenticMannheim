from uuid import uuid4

from domain.intersection import Intersection
from domain.road import Road, RoadPoint, RoadType

from .osm import OSMNode, OSMRoad


class OSMMapper:
    def map_roads(
        self,
        osm_roads: list[OSMRoad],
    ) -> tuple[list[Road], list[Intersection]]:
        node_usage: dict[int, int] = {}

        # 1. Count usage across all roads
        for road in osm_roads:
            for node in road.nodes:
                node_usage[node.id] = (
                    node_usage.get(node.id, 0) + 1
                )

        # 2. An intersection MUST be created for:
        # - Any node shared by >= 2 roads (usage > 1)
        # - The start and end nodes of EVERY road (endpoints/dead ends)
        intersection_nodes = {
            node_id
            for node_id, usage in node_usage.items()
            if usage > 1
        }

        for road in osm_roads:
            if road.nodes:
                intersection_nodes.add(road.nodes[0].id)
                intersection_nodes.add(road.nodes[-1].id)

        # 3. Create Intersection domain entities
        intersections_by_node: dict[int, Intersection] = {}

        for road in osm_roads:
            for node in road.nodes:
                if node.id in intersection_nodes and node.id not in intersections_by_node:
                    intersections_by_node[node.id] = (
                        self._create_intersection(node)
                    )

        # 4. Split roads at intersection boundaries
        roads: list[Road] = []

        for osm_road in osm_roads:
            roads.extend(
                self._split_road(
                    osm_road,
                    intersections_by_node,
                )
            )

        return (
            roads,
            list(intersections_by_node.values()),
        )

    def _split_road(
        self,
        osm_road: OSMRoad,
        intersections: dict[int, Intersection],
    ) -> list[Road]:
        segments: list[Road] = []
        current_nodes: list[OSMNode] = []

        for node in osm_road.nodes:
            current_nodes.append(node)

            is_intersection = node.id in intersections

            if (
                is_intersection
                and len(current_nodes) >= 2
            ):
                segments.append(
                    self._create_road_segment(
                        osm_road,
                        current_nodes,
                        intersections,
                    )
                )

                current_nodes = [node]

        return segments

    def _create_road_segment(
        self,
        osm_road: OSMRoad,
        nodes: list[OSMNode],
        intersections: dict[int, Intersection],
    ) -> Road:
        start_node = nodes[0]
        end_node = nodes[-1]

        start_intersection = intersections.get(
            start_node.id
        )

        end_intersection = intersections.get(
            end_node.id
        )

        if (
            start_intersection is None
            or end_intersection is None
        ):
            raise ValueError(
                "Road segment must start and end at "
                "an intersection."
            )

        geometry = tuple(
            RoadPoint(
                latitude=node.latitude,
                longitude=node.longitude,
            )
            for node in nodes
        )

        return Road(
            id=uuid4(),
            name=osm_road.name,
            road_type=self._map_road_type(
                osm_road.road_type
            ),
            start_intersection_id=start_intersection.id,
            end_intersection_id=end_intersection.id,
            length_meters=self._calculate_length(
                geometry
            ),
            speed_limit_kmh=osm_road.speed_limit_kmh,
            lanes=osm_road.lanes,
            geometry=geometry,
        )

    @staticmethod
    def _create_intersection(
        node: OSMNode,
    ) -> Intersection:
        return Intersection(
            intersection_id=uuid4(),
            name=f"OSM Node {node.id}",
            latitude=node.latitude,
            longitude=node.longitude,
        )

    @staticmethod
    def _map_road_type(
        value: str,
    ) -> RoadType:
        try:
            return RoadType(value)
        except ValueError:
            return RoadType.SERVICE

    @staticmethod
    def _calculate_length(
        geometry: tuple[RoadPoint, ...],
    ) -> float:
        total = 0.0

        for first, second in zip(
            geometry,
            geometry[1:],
        ):
            latitude_distance = (
                second.latitude
                - first.latitude
            ) * 111_000

            longitude_distance = (
                second.longitude
                - first.longitude
            ) * 111_000

            total += (
                latitude_distance**2
                + longitude_distance**2
            ) ** 0.5

        return total