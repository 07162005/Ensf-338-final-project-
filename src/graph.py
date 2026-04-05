from models import Route


class Graph:
    def __init__(self, campus):
        self.campus = campus

    def add_edge(self, source_id: str, destination_id: str, weight: float):
        """Add an undirected edge between two buildings with given weight."""
        if source_id not in self.campus.pathways:
            self.campus.pathways[source_id] = []
        if destination_id not in self.campus.pathways:
            self.campus.pathways[destination_id] = []

        self.campus.pathways[source_id].append((destination_id, weight))
        self.campus.pathways[destination_id].append((source_id, weight))

    def load_map_from_file(self, filename: str):
        """
        Load campus map from a file.
        Expected format: source_id,destination_id,weight (one per line)
        Example: ICT,ENG,5
        """
        try:
            with open(filename, 'r') as file:
                for line_num, line in enumerate(file, 1):
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    parts = line.split(',')
                    if len(parts) != 3:
                        print(f"Warning: Line {line_num} has invalid format, skipping: {line}")
                        continue
                    
                    source_id = parts[0].strip()
                    destination_id = parts[1].strip()
                    
                    try:
                        weight = float(parts[2].strip())
                        if weight <= 0:
                            print(f"Warning: Line {line_num} has non-positive weight, skipping: {line}")
                            continue
                    except ValueError:
                        print(f"Warning: Line {line_num} has invalid weight, skipping: {line}")
                        continue
                    
                    self.add_edge(source_id, destination_id, weight)
                    
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            raise
        except Exception as e:
            print(f"Error reading file '{filename}': {e}")
            raise

    def shortest_path(self, source_id: str, destination_id: str):
        """
        Find the shortest path between two buildings using Dijkstra's algorithm.
        Returns a Route object containing the path and total distance.
        """
        if source_id not in self.campus.pathways:
            raise ValueError(f"Source building '{source_id}' not found in campus map")
        if destination_id not in self.campus.pathways:
            raise ValueError(f"Destination building '{destination_id}' not found in campus map")
        
        distances = {node: float('inf') for node in self.campus.pathways}
        previous = {node: None for node in self.campus.pathways}
        unvisited = set(self.campus.pathways.keys())
        
        distances[source_id] = 0
        
        while unvisited:
            current_node = self._get_smallest_unvisited(distances, unvisited)
            
            if current_node is None:
                break
            
            if current_node == destination_id:
                break
            
            unvisited.remove(current_node)
            
            if current_node in self.campus.pathways:
                for neighbor, weight in self.campus.pathways[current_node]:
                    if neighbor in unvisited:
                        new_distance = distances[current_node] + weight
                        if new_distance < distances[neighbor]:
                            distances[neighbor] = new_distance
                            previous[neighbor] = current_node
        
        if distances[destination_id] == float('inf'):
            raise ValueError(f"No path exists between {source_id} and {destination_id}")
        
        path = self._reconstruct_path(previous, source_id, destination_id)
        
        return Route(source_id, destination_id, path, distances[destination_id])

    def _get_smallest_unvisited(self, distances: dict, unvisited: set):
        """
        Return the unvisited node with smallest known distance.
        """
        min_distance = float('inf')
        min_node = None
        
        for node in unvisited:
            if distances[node] < min_distance:
                min_distance = distances[node]
                min_node = node
        
        return min_node

    def _reconstruct_path(self, previous: dict, source_id: str, destination_id: str):
        """
        Reconstruct the final path from previous map.
        Returns a list of building IDs from source to destination.
        """
        path = []
        current = destination_id
        
        while current is not None:
            path.append(current)
            current = previous.get(current)
        
        path.reverse()
        
        if path and path[0] != source_id:
            raise ValueError("Path reconstruction failed: Source not at beginning of path")
        
        return path
    
    def get_all_buildings(self):
        """Return a list of all building IDs in the graph."""
        return list(self.campus.pathways.keys())
    
    def get_neighbors(self, building_id: str):
        """Return all neighbors of a building with their edge weights."""
        if building_id in self.campus.pathways:
            return self.campus.pathways[building_id].copy()
        return []