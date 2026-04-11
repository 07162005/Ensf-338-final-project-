from models import Building, Room, Campus, Booking, NavigationSession, ServiceRequest, IncomingRequest
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

    # Sample buildings
    ict = Building("ICT", "ICT Building", (0, 0))
    eng = Building("ENG", "Engineering Building", (2, 1))

    ict.add_room(Room("ICT-121", 120, "lecture"))

    campus.add_building(ict)
    campus.add_building(eng)

    graph.add_edge("ICT", "ENG", 5)

    session = NavigationSession("user1")

    while True:
        print("\n===== MENU =====")
        print("1. Find shortest path")
        print("2. Undo last navigation")
        print("3. Add booking")
        print("4. View bookings for a day")
        print("5. Query bookings by time range")
        print("6. Add service request")
        print("7. Serve next service request")
        print("8. Enqueue incoming request")
        print("9. Process next incoming request")
        print("10. Exit")

        choice = input("Enter choice: ")

        # 1. Shortest path
        if choice == "1":
            src = input("Enter source building: ")
            dest = input("Enter destination building: ")

            try:
                route = navigation_manager.navigate(session, src, dest)
                print("Path:", " -> ".join(route.path))
                print("Total distance:", route.total_weight)
            except Exception as e:
                print("Error:", e)

        # 2. Undo navigation
        elif choice == "2":
            navigation_manager.undo_last_navigation(session)

        # 3. Add booking
        elif choice == "3":
            booking_id = input("Booking ID: ")
            room_id = input("Room ID: ")
            title = input("Event title: ")
            date = input("Date (YYYY-MM-DD): ")
            start = int(input("Start time (minutes): "))
            end = int(input("End time (minutes): "))
            organizer = input("Organizer: ")

            booking = Booking(booking_id, room_id, title, date, start, end, organizer)
            success = booking_system.add_booking(booking)

            if success:
                print("Booking added successfully")
            else:
                print("Booking failed")

        # 4. View bookings for a day
        elif choice == "4":
            date = input("Enter date: ")
            bookings = booking_system.get_bookings_for_day(date)

            if not bookings:
                print("No bookings found")
            else:
                for b in bookings:
                    print(b.event_title, "|", b.start_time, "-", b.end_time)

        # 5. Query bookings by time range
        elif choice == "5":
            date = input("Enter date: ")
            start = int(input("Start time: "))
            end = int(input("End time: "))

            bookings = booking_system.get_bookings_in_time_range(date, start, end)

            if not bookings:
                print("No bookings found")
            else:
                for b in bookings:
                    print(b.event_title, "|", b.start_time, "-", b.end_time)

        # 6. Add service request (priority queue)
        elif choice == "6":
            request_id = input("Request ID: ")
            name = input("Requester name: ")
            service = input("Service type: ")
            desc = input("Description: ")
            priority = int(input("Priority (3=High, 2=Medium, 1=Low): "))
            timestamp = len(priority_queue.requests) + 1

            req = ServiceRequest(request_id, name, service, desc, priority, timestamp)
            priority_queue.add_request(req)
            print("Service request added")

        # 7. Serve next service request
        elif choice == "7":
            req = priority_queue.serve_next()
            if req:
                print("Serving:", req.request_id, "| Priority:", req.priority)

        # 8. Enqueue incoming request
        elif choice == "8":
            request_id = input("Request ID: ")
            rtype = input("Type (navigation/service): ")
            order = len(request_queue.queue) + 1

            req = IncomingRequest(request_id, rtype, None, order)
            request_queue.enqueue(req)
            print("Request added to queue")

        # 9. Process next incoming request
        elif choice == "9":
            req = request_queue.dequeue()
            if req:
                print("Processed:", req.request_id)

        # 10. Exit
        elif choice == "10":
            print("Exiting...")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()