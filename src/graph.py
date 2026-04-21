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
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                source, destination, weight = [part.strip() for part in line.split(",")]
                self.add_edge(source, destination, float(weight))

    def shortest_path(self, source_id: str, destination_id: str):
        if source_id not in self.campus.pathways or destination_id not in self.campus.pathways:
            return None

        distances = {}
        previous = {}
        visited = []

        for node in self.campus.pathways:
            distances[node] = float("inf")
            previous[node] = None
        distances[source_id] = 0

        while len(visited) < len(self.campus.pathways):
            current = None
            current_distance = float("inf")

            for node in self.campus.pathways:
                if node not in visited and distances[node] < current_distance:
                    current = node
                    current_distance = distances[node]

            if current is None:
                break

            if current == destination_id:
                break

            visited.append(current)

            for neighbor, weight in self.campus.pathways[current]:
                if neighbor in visited:
                    continue
                new_distance = distances[current] + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current

        if distances[destination_id] == float("inf"):
            return None

        path = []
        current = destination_id
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()

        return Route(source_id, destination_id, path, distances[destination_id])