class LookupManager:
    def __init__(self, campus):
        self.campus = campus

    def insert_building(self, building):
        self.campus.buildings.put(building.building_id, building)

        if building.building_id not in self.campus.pathways:
            self.campus.pathways[building.building_id] = []

    def lookup_building(self, building_id: str):
        return self.campus.buildings.get(building_id)

    def delete_building(self, building_id: str):
        removed_building = self.campus.buildings.remove(building_id)

        if removed_building is None:
            return False

        if building_id in self.campus.pathways:
            del self.campus.pathways[building_id]

        for source in self.campus.pathways:
            new_neighbors = []

            for neighbor, weight in self.campus.pathways[source]:
                if neighbor != building_id:
                    new_neighbors.append((neighbor, weight))

            self.campus.pathways[source] = new_neighbors

        return True

    def insert_room(self, building_id: str, room):
        building = self.lookup_building(building_id)

        if building is None:
            return False

        building.rooms.put(room.room_id, room)
        return True

    def lookup_room(self, building_id: str, room_id: str):
        building = self.lookup_building(building_id)

        if building is None:
            return None

        return building.rooms.get(room_id)

    def delete_room(self, building_id: str, room_id: str):
        building = self.lookup_building(building_id)

        if building is None:
            return False

        removed_room = building.rooms.remove(room_id)
        return removed_room is not None