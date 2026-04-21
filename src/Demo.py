from models import Campus, Building, Room, Booking, ServiceRequest, IncomingRequest
from graph import Graph
from booking_system import BookingSystem
from queues import PriorityServiceQueue, RequestQueue
from lookup import LookupManager
from HelperFunctions import parse_location, time_to_minutes


def build_demo_system(data_dir):
    campus = Campus()
    graph = Graph(campus)
    booking_system = BookingSystem()
    priority_queue = PriorityServiceQueue()
    request_queue = RequestQueue()
    lookup = LookupManager(campus)

    with open(f"{data_dir}/buildings.txt", "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            building_id, name, location = [part.strip() for part in line.split(",")]
            building = Building(building_id, name, parse_location(location))
            lookup.insert_building(building)

    with open(f"{data_dir}/rooms.txt", "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            building_id, room_id, capacity, room_type = [part.strip() for part in line.split(",")]
            room = Room(room_id, int(capacity), room_type)
            lookup.insert_room(building_id, room)

    graph.load_map_from_file(f"{data_dir}/campus_map.txt")

    with open(f"{data_dir}/bookings.txt", "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            booking_id, room_id, title, date, start, end, organizer = [part.strip() for part in line.split(",")]
            booking = Booking(
                booking_id,
                room_id,
                title,
                date,
                time_to_minutes(start),
                time_to_minutes(end),
                organizer,
            )

            booking_system.add_booking(booking)

            building_id = room_id.split("-")[0]
            room = lookup.lookup_room(building_id, room_id)

            if room is not None:
                room.bookings.append(booking)

    with open(f"{data_dir}/service_requests.txt", "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            request_id, requester_name, service_type, description, priority, timestamp = [part.strip() for part in line.split(",")]
            request = ServiceRequest(
                request_id,
                requester_name,
                service_type,
                description,
                int(priority),
                int(timestamp)
            )
            priority_queue.add_request(request)

    with open(f"{data_dir}/incoming_requests.txt", "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            request_id, request_type, payload, arrival_order = [part.strip() for part in line.split(",", 3)]
            request = IncomingRequest(
                request_id,
                request_type,
                payload,
                int(arrival_order)
            )
            request_queue.enqueue(request)

    return campus, graph, booking_system, priority_queue, request_queue
