from hashmap import HashMap


class Room:
    def __init__(self, room_id: str, capacity: int, room_type: str):
        self.room_id = room_id
        self.capacity = capacity
        self.room_type = room_type
        self.bookings = []  # list of Booking objects


class Building:
    def __init__(self, building_id: str, name: str, location: tuple):
        self.building_id = building_id
        self.name = name
        self.location = location
        self.rooms = HashMap()   # custom hash map


class Campus:
    def __init__(self):
        self.buildings = HashMap()   # custom hash map
        self.pathways = {}           # adjacency list graph


class Booking:
    def __init__(self, booking_id: str, room_id: str, event_title: str,
                 event_date: str, start_time: int, end_time: int, organizer: str):
        self.booking_id = booking_id
        self.room_id = room_id
        self.event_title = event_title
        self.event_date = event_date
        self.start_time = start_time
        self.end_time = end_time
        self.organizer = organizer


class Route:
    def __init__(self, source_id: str, destination_id: str, path: list, total_weight: float):
        self.source_id = source_id
        self.destination_id = destination_id
        self.path = path
        self.total_weight = total_weight


class NavigationSession:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.current_location = None
        self.history = []
        self.undo_limit = 10


class ServiceRequest:
    def __init__(self, request_id: str, requester_name: str, service_type: str,
                 description: str, priority: int, timestamp: int):
        self.request_id = request_id
        self.requester_name = requester_name
        self.service_type = service_type
        self.description = description
        self.priority = priority
        self.timestamp = timestamp


class IncomingRequest:
    def __init__(self, request_id: str, request_type: str, payload: str, arrival_order: int):
        self.request_id = request_id
        self.request_type = request_type
        self.payload = payload
        self.arrival_order = arrival_order


class AVLNode:
    def __init__(self, key, booking):
        self.key = key
        self.booking = booking
        self.left = None
        self.right = None
        self.height = 1