from models import (
    Building,
    Room,
    Campus,
    Booking,
    NavigationSession,
    ServiceRequest,
    IncomingRequest,
)
from graph import Graph
from navigation import NavigationManager
from Booking_system import BookingSystem
from queue import RequestQueue, PriorityServiceQueue


class CampusNavigationApp:
    """
    Central integration layer for the Campus Navigation and Event Management System.
    Owns all major components and provides clean methods for the CLI to use.
    """

    def __init__(self):
        self.campus = Campus()
        self.graph = Graph(self.campus)
        self.navigation_manager = NavigationManager(self.graph)
        self.booking_system = BookingSystem()
        self.request_queue = RequestQueue()
        self.priority_queue = PriorityServiceQueue()
        self.session = NavigationSession("user1")

        self._build_sample_campus()
        self._seed_sample_bookings()

    
    # Setup / Initialization
    

    def _build_sample_campus(self):
        buildings_data = [
            ("LIB", "Library", (0, 3)),
            ("SCI", "Science A", (3, 3)),
            ("ICT", "ICT Building", (0, 1)),
            ("ENG", "Engineering Block", (3, 1)),
            ("GYM", "Gym", (6, 2)),
            ("SU", "Student Union", (0, -1)),
            ("PKD", "Parkade", (2, -1)),
            ("MFH", "MacEwan Hall", (4, -1)),
            ("RES", "Residence", (0, -4)),
            ("ADMIN", "Administration", (-2, 2)),
            ("BUS", "Business", (5, 4)),
            ("ART", "Arts", (-3, 0)),
            ("LAW", "Law", (6, 0)),
            ("MED", "Medicine", (8, 2)),
            ("FIELD", "Athletic Field", (7, -2)),
        ]

        for building_id, name, location in buildings_data:
            building = Building(building_id, name, location)
            building.add_room(Room(f"{building_id}-101", 60, "lecture"))
            building.add_room(Room(f"{building_id}-201", 30, "lab"))
            building.add_room(Room(f"{building_id}-301", 12, "office"))
            self.campus.add_building(building)

        edges = [
            ("LIB", "SCI", 3),
            ("LIB", "ICT", 4),
            ("SCI", "ENG", 2),
            ("SCI", "GYM", 5),
            ("ICT", "ENG", 6),
            ("ICT", "SU", 3),
            ("ICT", "PKD", 7),
            ("ENG", "MFH", 2),
            ("SU", "RES", 5),
            ("ADMIN", "LIB", 3),
            ("ADMIN", "ART", 2),
            ("ART", "SU", 4),
            ("SCI", "BUS", 3),
            ("BUS", "GYM", 3),
            ("ENG", "LAW", 4),
            ("LAW", "MED", 3),
            ("LAW", "FIELD", 3),
            ("MFH", "FIELD", 4),
            ("PKD", "FIELD", 6),
            ("BUS", "MED", 4),
            ("RES", "ART", 6),
            ("SU", "PKD", 2),
            ("PKD", "MFH", 3),
            ("ENG", "BUS", 4),
            ("GYM", "MED", 2),
        ]

        for source, destination, weight in edges:
            self.graph.add_edge(source, destination, weight)

    def _seed_sample_bookings(self):
        sample_bookings = [
            Booking("B001", "ICT-101", "Data Structures Lecture", "2026-04-15", 540, 630, "Prof. Smith"),
            Booking("B002", "ENG-101", "Capstone Team Meeting", "2026-04-15", 660, 720, "Team Alpha"),
            Booking("B003", "LIB-201", "Study Group", "2026-04-15", 780, 840, "Amitesh"),
            Booking("B004", "SCI-101", "Chemistry Seminar", "2026-04-16", 600, 690, "Dr. Lee"),
            Booking("B005", "SU-101", "Club Event", "2026-04-16", 900, 1020, "Student Union"),
            Booking("B006", "ICT-201", "Python Workshop", "2026-04-17", 570, 660, "ENSF Team"),
            Booking("B007", "ENG-201", "Design Review", "2026-04-17", 720, 780, "Project Group"),
            Booking("B008", "MFH-101", "Guest Speaker", "2026-04-17", 840, 930, "Faculty Office"),
        ]

        for booking in sample_bookings:
            self.booking_system.add_booking(booking)

   
    # Utility / Read helpers
    

    def get_all_buildings(self):
        return [self.campus.buildings[key] for key in sorted(self.campus.buildings.keys())]

    def get_all_pathways(self):
        edges = []
        seen = set()

        for source, neighbors in self.campus.pathways.items():
            for destination, weight in neighbors:
                edge_key = tuple(sorted((source, destination)))
                if edge_key not in seen:
                    seen.add(edge_key)
                    edges.append((source, destination, weight))

        return sorted(edges)

    def lookup_building(self, building_id: str):
        return self.campus.get_building(building_id.upper())

    def lookup_room(self, building_id: str, room_id: str):
        building = self.lookup_building(building_id)
        if building is None:
            return None
        return building.get_room(room_id.upper())

   
    # Navigation
    

    def find_shortest_path(self, source_id: str, destination_id: str):
        return self.navigation_manager.navigate(
            self.session,
            source_id.upper(),
            destination_id.upper()
        )

    def undo_navigation(self):
        success = self.navigation_manager.undo_last_navigation(self.session)
        current_location = self.navigation_manager.get_current_location(self.session)
        return success, current_location

    def get_navigation_history(self):
        return self.navigation_manager.get_navigation_history(self.session)


    # Booking System
    

    def add_booking(
        self,
        booking_id: str,
        room_id: str,
        title: str,
        event_date: str,
        start_time: int,
        end_time: int,
        organizer: str,
    ):
        room_id = room_id.upper()

        if "-" not in room_id:
            return False

        building_id = room_id.split("-")[0]
        building = self.lookup_building(building_id)

        if building is None:
            return False

        room = building.get_room(room_id)
        if room is None:
            return False

        booking = Booking(
            booking_id,
            room_id,
            title,
            event_date,
            start_time,
            end_time,
            organizer,
        )

        return self.booking_system.add_booking(booking)

    def remove_booking(self, booking_id: str):
        return self.booking_system.remove_booking(booking_id)

    def get_bookings_for_day(self, event_date: str):
        return self.booking_system.get_bookings_for_day(event_date)

    def get_bookings_in_time_range(self, event_date: str, start_time: int, end_time: int):
        return self.booking_system.get_bookings_in_time_range(event_date, start_time, end_time)

    def get_next_upcoming_event(self):
        return self.booking_system.get_next_upcoming_event()

    
    # Priority Service Queue
    

    def add_service_request(
        self,
        request_id: str,
        requester_name: str,
        service_type: str,
        description: str,
        priority: int,
    ):
        timestamp = len(self.priority_queue.requests) + 1
        request = ServiceRequest(
            request_id,
            requester_name,
            service_type,
            description,
            priority,
            timestamp,
        )
        self.priority_queue.add_request(request)

    def serve_next_service_request(self):
        return self.priority_queue.serve_next()

    
    # FIFO Incoming Request Pipeline
    

    def enqueue_incoming_request(self, request_id: str, request_type: str, payload: str):
        arrival_order = len(self.request_queue.queue) + 1
        request = IncomingRequest(
            request_id,
            request_type,
            payload,
            arrival_order,
        )
        self.request_queue.enqueue(request)

    def process_next_incoming_request(self):
        return self.request_queue.dequeue()

    def load_demo_requests(self, count: int = 20):
        for i in range(1, count + 1):
            if i % 2 == 0:
                request_type = "navigation"
                payload = f"Route query #{i}"
            else:
                request_type = "service"
                payload = f"Service ticket #{i}"

            self.enqueue_incoming_request(
                f"Q{i:03d}",
                request_type,
                payload,
            )


# Demo helper functions

    def _format_minutes(self, minutes: int) -> str:
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours:02d}:{mins:02d}"

    def reset_demo_state(self):
        """
        Reset mutable runtime state so demo mode produces the same output
        each time it is run in a fresh, predictable way.
        """
        self.session = NavigationSession("user1")
        self.request_queue = RequestQueue()
        self.priority_queue = PriorityServiceQueue()

    def run_demo(self):
        self.reset_demo_state()

        print("\n================ DEMO MODE START ================\n")

       
        # 1. Shortest path queries
      
        print("1) SHORTEST PATH DEMO")
        route1 = self.find_shortest_path("LIB", "MED")
        print(f"Route 1: {' -> '.join(route1.path)}")
        print(f"Total walking time: {route1.total_weight} minutes\n")

        route2 = self.find_shortest_path("ICT", "GYM")
        print(f"Route 2: {' -> '.join(route2.path)}")
        print(f"Total walking time: {route2.total_weight} minutes\n")

        
        # 2. Undo navigation + history
        
        print("2) UNDO NAVIGATION DEMO")
        success, current = self.undo_navigation()
        print(f"Undo successful: {success}")
        print(f"Current location after undo: {current}\n")

        print("Navigation history:")
        history = self.get_navigation_history()
        if not history:
            print("No navigation history.\n")
        else:
            for i, record in enumerate(history, start=1):
                route = record["route"]
                print(
                    f"{i}. {record['source']} -> {record['destination']} | "
                    f"Path: {' -> '.join(route.path)} | "
                    f"Cost: {route.total_weight}"
                )
            print()

        
        # 3. Booking range query
      
        print("3) BOOKING RANGE QUERY DEMO")
        date = "2026-04-15"
        start = 500
        end = 800
        bookings = self.get_bookings_in_time_range(date, start, end)
        print(
            f"Bookings on {date} between "
            f"{self._format_minutes(start)} and {self._format_minutes(end)}:"
        )
        if not bookings:
            print("No bookings found.\n")
        else:
            for booking in bookings:
                print(
                    f"[{booking.booking_id}] {booking.event_title} | Room: {booking.room_id} | "
                    f"{self._format_minutes(booking.start_time)}-{self._format_minutes(booking.end_time)} | "
                    f"Organizer: {booking.organizer}"
                )
            print()

        
        # 4. Priority queue demo
        
        print("4) PRIORITY QUEUE DEMO")
        self.add_service_request("SR001", "Alice", "IT Support", "Projector failure", 2)
        self.add_service_request("SR002", "Bob", "Maintenance", "Water leak in lab", 3)
        self.add_service_request("SR003", "Charlie", "General Help", "Need room unlock", 1)

        print("Serving requests in priority order:")
        while True:
            request = self.serve_next_service_request()
            if request is None:
                break
            print(
                f"{request.request_id} | {request.requester_name} | "
                f"{request.service_type} | Priority {request.priority}"
            )
        print()

       
        # 5. Fast lookup demo
        
        print("5) FAST LOOKUP DEMO")

        building = self.lookup_building("ICT")
        if building is not None:
            print(f"Building lookup ICT: {building.name} at {building.location}")
        else:
            print("Building lookup ICT failed")

        room = self.lookup_room("ICT", "ICT-101")
        if room is not None:
            print(
                f"Room lookup ICT-101: capacity={room.capacity}, type={room.room_type}"
            )
        else:
            print("Room lookup ICT-101 failed")

        missing_building = self.lookup_building("FAKE")
        if missing_building is None:
            print("Building lookup FAKE: not found")
        else:
            print("Building lookup FAKE unexpectedly succeeded")
        print()

        
        # 6. FIFO request pipeline demo
     
        print("6) FIFO REQUEST PIPELINE DEMO")
        self.load_demo_requests(20)
        print("Loaded 20 sequential incoming requests.")
        print("Processing first 5 requests in arrival order:")

        for _ in range(5):
            request = self.process_next_incoming_request()
            if request is None:
                break
            print(
                f"{request.request_id} | {request.request_type} | "
                f"{request.payload} | Arrival #{request.arrival_order}"
            )

        print("DEMO MODE END\n")