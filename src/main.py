from models import Building, Room, Campus, Booking, NavigationSession
from graph import Graph
from navigation import NavigationManager
from Booking_system import BookingSystem
from queue import RequestQueue, PriorityServiceQueue


def main():
    campus = Campus()
    graph = Graph(campus)
    navigation_manager = NavigationManager(graph)
    booking_system = BookingSystem()
    request_queue = RequestQueue()
    priority_queue = PriorityServiceQueue()

    # Example setup
    ict = Building("ICT", "Information and Communications Technology", (0, 0))
    eng = Building("ENG", "Engineering Building", (2, 1))

    ict.add_room(Room("ICT-121", 120, "lecture"))
    ict.add_room(Room("ICT-102", 30, "lab"))

    campus.add_building(ict)
    campus.add_building(eng)

    graph.add_edge("ICT", "ENG", 5)

    session = NavigationSession("user1")

    # TODO:
    # Add menu loop here
    #
    # Suggested menu options:
    # 1. Load campus map from file
    # 2. Find shortest path
    # 3. Undo last navigation
    # 4. Add booking
    # 5. Remove booking
    # 6. Query bookings by time range
    # 7. Add service request
    # 8. Serve next service request
    # 9. Enqueue incoming request
    # 10. Process next incoming request
    # 11. Exit

    print("Campus Navigation and Event Management System starter loaded.")


if __name__ == "__main__":
    main()
