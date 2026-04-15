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
            # April 15
            Booking("B001", "ICT-101", "Data Structures Lecture", "2026-04-15", 540, 630, "Prof. Smith"),
            Booking("B002", "ENG-101", "Capstone Team Meeting", "2026-04-15", 660, 720, "Team Alpha"),
            Booking("B003", "LIB-201", "Study Group", "2026-04-15", 780, 840, "Amitesh"),
            Booking("B004", "SCI-101", "Chemistry Seminar", "2026-04-15", 480, 570, "Dr. Lee"),
            Booking("B005", "SU-101", "Club Orientation", "2026-04-15", 900, 1020, "Student Union"),
            Booking("B006", "GYM-101", "Fitness Workshop", "2026-04-15", 420, 510, "Rec Services"),
            Booking("B007", "ADMIN-101", "Budget Meeting", "2026-04-15", 600, 660, "Admin Office"),
            Booking("B008", "BUS-101", "Entrepreneurship Talk", "2026-04-15", 720, 810, "Biz Club"),
            Booking("B009", "ART-101", "Gallery Opening", "2026-04-15", 840, 960, "Arts Dept"),
            Booking("B010", "LAW-101", "Moot Court Practice", "2026-04-15", 480, 600, "Law Society"),
            # April 16
            Booking("B011", "ICT-201", "Python Workshop", "2026-04-16", 570, 660, "ENSF Team"),
            Booking("B012", "ENG-201", "Design Review", "2026-04-16", 720, 780, "Project Group"),
            Booking("B013", "MFH-101", "Guest Speaker", "2026-04-16", 840, 930, "Faculty Office"),
            Booking("B014", "LIB-101", "Research Methods", "2026-04-16", 480, 570, "Prof. Adams"),
            Booking("B015", "SCI-201", "Biology Lab", "2026-04-16", 600, 720, "Dr. Patel"),
            Booking("B016", "SU-201", "Student Council", "2026-04-16", 780, 840, "SU President"),
            Booking("B017", "GYM-201", "Yoga Session", "2026-04-16", 420, 480, "Wellness Ctr"),
            Booking("B018", "ADMIN-201", "HR Training", "2026-04-16", 540, 660, "HR Dept"),
            Booking("B019", "BUS-201", "Finance Seminar", "2026-04-16", 660, 750, "Prof. Chen"),
            Booking("B020", "ART-201", "Sculpture Class", "2026-04-16", 480, 600, "Prof. Rivera"),
            # April 17
            Booking("B021", "ICT-101", "Algorithms Lecture", "2026-04-17", 480, 570, "Prof. Smith"),
            Booking("B022", "ENG-101", "Robotics Demo", "2026-04-17", 600, 690, "Robotics Club"),
            Booking("B023", "LIB-201", "Exam Prep Session", "2026-04-17", 720, 840, "Tutoring Ctr"),
            Booking("B024", "SCI-101", "Physics Lab", "2026-04-17", 480, 600, "Dr. Nguyen"),
            Booking("B025", "MED-101", "First Aid Training", "2026-04-17", 540, 660, "Health Svcs"),
            Booking("B026", "LAW-201", "Contract Law Lecture", "2026-04-17", 660, 780, "Prof. Moore"),
            Booking("B027", "BUS-101", "Marketing Workshop", "2026-04-17", 780, 870, "Mktg Dept"),
            Booking("B028", "GYM-101", "Basketball Practice", "2026-04-17", 900, 1020, "Athletics"),
            Booking("B029", "ADMIN-101", "Board Meeting", "2026-04-17", 480, 600, "President"),
            Booking("B030", "RES-101", "RA Training", "2026-04-17", 600, 660, "Housing Dept"),
            # April 18
            Booking("B031", "ICT-201", "Web Dev Lab", "2026-04-18", 480, 600, "Prof. Kim"),
            Booking("B032", "ENG-201", "Thermodynamics", "2026-04-18", 540, 630, "Dr. Hassan"),
            Booking("B033", "LIB-101", "Writing Workshop", "2026-04-18", 660, 780, "Writing Ctr"),
            Booking("B034", "SCI-201", "Chemistry Lab", "2026-04-18", 480, 600, "Dr. Lee"),
            Booking("B035", "SU-101", "Club Fair", "2026-04-18", 720, 900, "Student Union"),
            Booking("B036", "MED-101", "Anatomy Lecture", "2026-04-18", 480, 570, "Dr. Osei"),
            Booking("B037", "LAW-101", "Legal Ethics", "2026-04-18", 600, 690, "Prof. White"),
            Booking("B038", "BUS-201", "Accounting Lab", "2026-04-18", 660, 750, "Prof. Gupta"),
            Booking("B039", "ART-101", "Painting Studio", "2026-04-18", 780, 900, "Prof. Diaz"),
            Booking("B040", "GYM-201", "Swimming Lessons", "2026-04-18", 480, 570, "Aquatics"),
            # April 19
            Booking("B041", "ICT-101", "OS Concepts Lecture", "2026-04-19", 480, 570, "Prof. Park"),
            Booking("B042", "ENG-101", "Civil Eng Seminar", "2026-04-19", 600, 690, "Dr. Torres"),
            Booking("B043", "LIB-201", "Thesis Writing Group", "2026-04-19", 720, 840, "Grad Studies"),
            Booking("B044", "SCI-101", "Genetics Lecture", "2026-04-19", 480, 600, "Dr. Yamamoto"),
            Booking("B045", "MFH-201", "Film Screening", "2026-04-19", 900, 1080, "Film Society"),
            Booking("B046", "ADMIN-201", "Policy Review", "2026-04-19", 540, 660, "VP Academic"),
            Booking("B047", "BUS-101", "Case Study Session", "2026-04-19", 660, 780, "Prof. Chen"),
            Booking("B048", "RES-101", "Resident Social", "2026-04-19", 840, 960, "Housing Dept"),
            Booking("B049", "LAW-201", "Moot Court Finals", "2026-04-19", 480, 660, "Law Society"),
            Booking("B050", "GYM-101", "Volleyball Practice", "2026-04-19", 780, 900, "Athletics"),
            # April 20
            Booking("B051", "ICT-201", "Network Security Lab", "2026-04-20", 480, 600, "Prof. Smith"),
            Booking("B052", "ENG-201", "Structural Analysis", "2026-04-20", 540, 660, "Dr. Hassan"),
            Booking("B053", "LIB-101", "Study Hall", "2026-04-20", 600, 780, "Open Access"),
            Booking("B054", "SCI-201", "Microbiology Lab", "2026-04-20", 480, 630, "Dr. Patel"),
            Booking("B055", "SU-101", "Town Hall Meeting", "2026-04-20", 720, 840, "SU President"),
            Booking("B056", "MED-101", "Pharmacology Lecture", "2026-04-20", 480, 570, "Dr. Osei"),
            Booking("B057", "ART-201", "Art History Lecture", "2026-04-20", 600, 690, "Prof. Rivera"),
            Booking("B058", "BUS-201", "Investment Seminar", "2026-04-20", 660, 780, "Finance Club"),
            Booking("B059", "ADMIN-101", "Faculty Senate", "2026-04-20", 780, 900, "Provost"),
            Booking("B060", "RES-201", "Study Skills Workshop", "2026-04-20", 840, 930, "Acad Support"),
            # April 21
            Booking("B061", "ICT-101", "Database Systems", "2026-04-21", 480, 600, "Prof. Kim"),
            Booking("B062", "ENG-101", "Fluid Mechanics", "2026-04-21", 540, 660, "Dr. Torres"),
            Booking("B063", "LIB-201", "Peer Tutoring", "2026-04-21", 600, 720, "Tutoring Ctr"),
            Booking("B064", "SCI-101", "Ecology Seminar", "2026-04-21", 660, 750, "Dr. Nguyen"),
            Booking("B065", "MFH-101", "Awards Ceremony", "2026-04-21", 840, 1020, "Dean Office"),
            Booking("B066", "LAW-101", "Tort Law Lecture", "2026-04-21", 480, 600, "Prof. White"),
            Booking("B067", "BUS-101", "Startup Pitch Night", "2026-04-21", 900, 1080, "Biz Club"),
            Booking("B068", "GYM-101", "Soccer Practice", "2026-04-21", 720, 840, "Athletics"),
            Booking("B069", "ADMIN-201", "Strategic Planning", "2026-04-21", 540, 660, "VP Finance"),
            Booking("B070", "ART-101", "Photography Workshop", "2026-04-21", 600, 720, "Arts Society"),
            # April 22
            Booking("B071", "ICT-201", "AI & ML Seminar", "2026-04-22", 480, 600, "Prof. Park"),
            Booking("B072", "ENG-201", "Capstone Presentations", "2026-04-22", 540, 780, "Dept Head"),
            Booking("B073", "LIB-101", "Book Club", "2026-04-22", 720, 810, "Library Staff"),
            Booking("B074", "SCI-201", "Astronomy Lab", "2026-04-22", 480, 600, "Dr. Yamamoto"),
            Booking("B075", "SU-201", "Wellness Fair", "2026-04-22", 600, 780, "Health Svcs"),
            Booking("B076", "MED-101", "Physiology Lecture", "2026-04-22", 480, 570, "Dr. Osei"),
            Booking("B077", "LAW-201", "International Law", "2026-04-22", 600, 720, "Prof. Moore"),
            Booking("B078", "BUS-101", "Networking Mixer", "2026-04-22", 900, 1020, "Alumni Assoc"),
            Booking("B079", "RES-101", "Movie Night", "2026-04-22", 840, 1020, "Housing Dept"),
            Booking("B080", "GYM-201", "Tennis Practice", "2026-04-22", 720, 840, "Athletics"),
            # April 23
            Booking("B081", "ICT-101", "Software Testing", "2026-04-23", 480, 570, "Prof. Smith"),
            Booking("B082", "ENG-101", "Materials Science", "2026-04-23", 540, 660, "Dr. Hassan"),
            Booking("B083", "LIB-201", "Grad Colloquium", "2026-04-23", 600, 720, "Grad Studies"),
            Booking("B084", "SCI-101", "Biochemistry Lecture", "2026-04-23", 480, 600, "Dr. Lee"),
            Booking("B085", "MFH-201", "Comedy Night", "2026-04-23", 900, 1080, "SU Events"),
            Booking("B086", "ADMIN-101", "Accreditation Review", "2026-04-23", 540, 720, "Provost"),
            Booking("B087", "BUS-201", "Supply Chain Lecture", "2026-04-23", 660, 780, "Prof. Gupta"),
            Booking("B088", "ART-201", "Dance Rehearsal", "2026-04-23", 780, 960, "Dance Dept"),
            Booking("B089", "LAW-101", "Criminal Law Lecture", "2026-04-23", 480, 600, "Prof. White"),
            Booking("B090", "GYM-101", "Track Practice", "2026-04-23", 720, 840, "Athletics"),
            # April 24
            Booking("B091", "ICT-201", "Cloud Computing Lab", "2026-04-24", 480, 600, "Prof. Kim"),
            Booking("B092", "ENG-201", "Electrical Circuits", "2026-04-24", 540, 660, "Dr. Torres"),
            Booking("B093", "LIB-101", "Open Study Hours", "2026-04-24", 600, 840, "Open Access"),
            Booking("B094", "SCI-201", "Environmental Sci Lab", "2026-04-24", 480, 630, "Dr. Patel"),
            Booking("B095", "SU-101", "End of Year Gala", "2026-04-24", 900, 1140, "Student Union"),
            Booking("B096", "MED-201", "Public Health Seminar", "2026-04-24", 600, 690, "Dr. Nguyen"),
            Booking("B097", "LAW-201", "Thesis Defense", "2026-04-24", 480, 660, "Grad Studies"),
            Booking("B098", "BUS-101", "Career Fair Prep", "2026-04-24", 660, 780, "Career Svcs"),
            Booking("B099", "ART-101", "Year-End Exhibition", "2026-04-24", 780, 960, "Arts Dept"),
            Booking("B100", "GYM-201", "Championship Game", "2026-04-24", 840, 1020, "Athletics"),
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

    def delete_building(self, building_id: str):
        return self.campus.remove_building(building_id.upper())

    def delete_room(self, building_id: str, room_id: str):
        building = self.lookup_building(building_id)
        if building is None:
            return False
        return building.remove_room(room_id.upper())

   
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
