class Room:
    def __init__(self, room_id: str, capacity: int, room_type: str):
        self.room_id   = room_id      # e.g. "ICT-121"
        self.capacity  = capacity     # max occupancy
        self.room_type = room_type    # "lecture", "lab", "office"
        self.bookings  = []           # list of Booking objects
                                      # You will implement booking insertion/search logic elsewhere


class Building:
    def __init__(self, building_id: str, name: str, location: tuple):
        self.building_id = building_id   # e.g. "ICT"
        self.name        = name          # full building name
        self.location    = location      # grid coords or (lat, lon)
        self.rooms       = {}            # room_id -> Room

    def add_room(self, room: Room):
        self.rooms[room.room_id] = room

    def get_room(self, room_id: str):
        return self.rooms.get(room_id)


class Campus:
    def __init__(self):
        self.buildings = {}              # building_id -> Building
        self.pathways  = {}              # adjacency list:
                                         # {building_id: [(neighbor_id, weight), ...]}

    def add_building(self, building: Building):
        self.buildings[building.building_id] = building
        if building.building_id not in self.pathways:
            self.pathways[building.building_id] = []

    def get_building(self, building_id: str):
        return self.buildings.get(building_id)


class Booking:
    def __init__(
        self,
        booking_id: str,
        room_id: str,
        event_title: str,
        event_date: str,
        start_time: int,
        end_time: int,
        organizer: str
    ):
        self.booking_id  = booking_id
        self.room_id     = room_id
        self.event_title = event_title
        self.event_date  = event_date      # e.g. "2026-04-02"
        self.start_time  = start_time      # minutes from midnight
        self.end_time    = end_time        # minutes from midnight
        self.organizer   = organizer


class Route:
    def __init__(self, source_id: str, destination_id: str, path: list, total_weight: float):
        self.source_id      = source_id
        self.destination_id = destination_id
        self.path           = path
        self.total_weight   = total_weight


class NavigationSession:
    def __init__(self, user_id: str):
        self.user_id          = user_id
        self.current_location = None
        self.history          = []         # use this like a stack
        self.undo_limit       = 10


class ServiceRequest:
    def __init__(
        self,
        request_id: str,
        requester_name: str,
        service_type: str,
        description: str,
        priority: int,
        timestamp: int
    ):
        self.request_id     = request_id
        self.requester_name = requester_name
        self.service_type   = service_type
        self.description    = description
        self.priority       = priority     # 3=Emergency, 2=Standard, 1=Low
        self.timestamp      = timestamp    # used for tie-breaking


class IncomingRequest:
    def __init__(self, request_id: str, request_type: str, payload, arrival_order: int):
        self.request_id    = request_id
        self.request_type  = request_type  # "navigation" or "service"
        self.payload       = payload
        self.arrival_order = arrival_order


class BookingNode:
    def __init__(self, key, booking: Booking):
        self.key     = key                 # e.g. (event_date, start_time, booking_id)
        self.booking = booking
        self.left    = None
        self.right   = None


class AVLNode:
    def __init__(self, key, booking: Booking):
        self.key     = key
        self.booking = booking
        self.left    = None
        self.right   = None
        self.height  = 1