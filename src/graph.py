from models import Route


class Graph:
    def __init__(self, campus):
        self.campus = campus

    def add_edge(self, source_id: str, destination_id: str, weight: float):
        if source_id not in self.campus.pathways:
            self.campus.pathways[source_id] = []
        if destination_id not in self.campus.pathways:
            self.campus.pathways[destination_id] = []

        self.campus.pathways[source_id].append((destination_id, weight))
        self.campus.pathways[destination_id].append((source_id, weight))

    def load_map_from_file(self, filename: str):
        # TODO:
        # Read lines like: ICT,ENG,5
        # Parse source, destination, weight
        # Call add_edge(...)
        pass

    def shortest_path(self, source_id: str, destination_id: str):
        # TODO:
        # Implement Dijkstra's algorithm yourself
        #
        # Suggested dicts:
        # distances = {node: float('inf')}
        # previous  = {node: None}
        # visited   = {node: False}
        #
        # Steps:
        # 1. Set source distance = 0
        # 2. Repeatedly select smallest unvisited node
        # 3. Relax its neighbors
        # 4. Rebuild path
        #
        # Return a Route object
        pass

    def _get_smallest_unvisited(self, distances: dict, visited: dict):
        # TODO:
        # Return the unvisited node with smallest known distance
        pass

    def _reconstruct_path(self, previous: dict, source_id: str, destination_id: str):
        # TODO:
        # Reconstruct final path from previous map
        pass