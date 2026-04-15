from app import CampusNavigationApp
from models import Booking


def format_minutes(minutes: int) -> str:
    """Convert minutes from midnight to HH:MM format."""
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}:{mins:02d}"


def read_int(prompt: str, min_value=None, max_value=None) -> int:
    """Read an integer from input with validation."""
    while True:
        value = input(prompt).strip()
        try:
            number = int(value)
            if min_value is not None and number < min_value:
                print(f"Value must be at least {min_value}.")
                continue
            if max_value is not None and number > max_value:
                print(f"Value must be at most {max_value}.")
                continue
            return number
        except ValueError:
            print("Invalid integer. Try again.")


def print_route(route):
    """Print a route cleanly."""
    print("\n--- Shortest Path Result ---")
    print("Route:", " -> ".join(route.path))
    print(f"Total walking time: {route.total_weight} minutes")


def print_booking(booking: Booking):
    """Print one booking."""
    print(
        f"[{booking.booking_id}] {booking.event_title} | Room: {booking.room_id} | "
        f"Date: {booking.event_date} | "
        f"{format_minutes(booking.start_time)}-{format_minutes(booking.end_time)} | "
        f"Organizer: {booking.organizer}"
    )


def print_bookings(bookings, title: str):
    """Print a list of bookings."""
    print(f"\n--- {title} ---")
    if not bookings:
        print("No bookings found.")
        return

    for booking in bookings:
        print_booking(booking)


def show_buildings(app: CampusNavigationApp):
    print("\n--- Campus Buildings ---")
    for building in app.get_all_buildings():
        print(f"{building.building_id}: {building.name} | Location: {building.location}")


def show_pathways(app: CampusNavigationApp):
    print("\n--- Campus Pathways ---")
    for source, destination, weight in app.get_all_pathways():
        print(f"{source} <-> {destination} : {weight} min")


def lookup_building(app: CampusNavigationApp):
    building_id = input("Enter building ID: ").strip().upper()
    building = app.lookup_building(building_id)

    print("\n--- Building Lookup ---")
    if building is None:
        print("Building not found.")
        return

    print(f"ID: {building.building_id}")
    print(f"Name: {building.name}")
    print(f"Location: {building.location}")
    print("Rooms:")
    for room_id, room in building.rooms.items():
        print(f"  {room_id} | Capacity: {room.capacity} | Type: {room.room_type}")


def lookup_room(app: CampusNavigationApp):
    building_id = input("Enter building ID: ").strip().upper()
    room_id = input("Enter room ID: ").strip().upper()

    room = app.lookup_room(building_id, room_id)

    print("\n--- Room Lookup ---")
    if room is None:
        print("Building or room not found.")
        return

    print(f"Room ID: {room.room_id}")
    print(f"Capacity: {room.capacity}")
    print(f"Type: {room.room_type}")


def delete_building_menu(app: CampusNavigationApp):
    building_id = input("Enter building ID to delete: ").strip().upper()
    removed = app.delete_building(building_id)

    print("\n--- Delete Building ---")
    if removed:
        print(f"Building '{building_id}' deleted successfully.")
    else:
        print(f"Building '{building_id}' not found.")


def delete_room_menu(app: CampusNavigationApp):
    building_id = input("Enter building ID: ").strip().upper()
    room_id = input("Enter room ID to delete: ").strip().upper()
    removed = app.delete_room(building_id, room_id)

    print("\n--- Delete Room ---")
    if removed:
        print(f"Room '{room_id}' deleted successfully.")
    else:
        print(f"Building or room not found.")


def add_booking_menu(app: CampusNavigationApp):
    booking_id = input("Booking ID: ").strip()
    room_id = input("Room ID: ").strip().upper()
    title = input("Event title: ").strip()
    date = input("Date (YYYY-MM-DD): ").strip()
    start = read_int("Start time in minutes from midnight: ", 0, 1439)
    end = read_int("End time in minutes from midnight: ", start + 1, 1440)
    organizer = input("Organizer: ").strip()

    success = app.add_booking(
        booking_id,
        room_id,
        title,
        date,
        start,
        end,
        organizer,
    )

    if success:
        print("Booking added successfully.")
    else:
        print("Booking was not added.")


def remove_booking_menu(app: CampusNavigationApp):
    booking_id = input("Enter booking ID to remove: ").strip()
    removed = app.remove_booking(booking_id)

    if removed:
        print("Booking removed successfully.")
    else:
        print("Booking not found.")


def add_service_request_menu(app: CampusNavigationApp):
    request_id = input("Request ID: ").strip()
    requester_name = input("Requester name: ").strip()
    service_type = input("Service type: ").strip()
    description = input("Description: ").strip()
    priority = read_int("Priority (3=Emergency, 2=Standard, 1=Low): ", 1, 3)

    app.add_service_request(
        request_id,
        requester_name,
        service_type,
        description,
        priority,
    )
    print("Service request added.")


def serve_next_service_request(app: CampusNavigationApp):
    request = app.serve_next_service_request()
    if request is None:
        print("No service requests in the queue.")
        return

    print("\n--- Serving Service Request ---")
    print(f"Request ID: {request.request_id}")
    print(f"Requester: {request.requester_name}")
    print(f"Service Type: {request.service_type}")
    print(f"Description: {request.description}")
    print(f"Priority: {request.priority}")


def enqueue_incoming_request_menu(app: CampusNavigationApp):
    request_id = input("Request ID: ").strip()
    request_type = input("Type (navigation/service): ").strip().lower()
    payload = input("Payload/description: ").strip()

    app.enqueue_incoming_request(request_id, request_type, payload)
    print("Incoming request added to FIFO pipeline.")


def process_next_incoming_request(app: CampusNavigationApp):
    request = app.process_next_incoming_request()
    if request is None:
        print("No incoming requests in the pipeline.")
        return

    print("\n--- Processed Incoming Request ---")
    print(f"Request ID: {request.request_id}")
    print(f"Type: {request.request_type}")
    print(f"Payload: {request.payload}")
    print(f"Arrival Order: {request.arrival_order}")


def simulate_request_pipeline(app: CampusNavigationApp):
    app.load_demo_requests(20)
    print("20 sequential incoming requests added to the FIFO pipeline.")


def show_navigation_history(app: CampusNavigationApp):
    history = app.get_navigation_history()

    print("\n--- Navigation History ---")
    if not history:
        print("No navigation history.")
        return

    for i, record in enumerate(history, start=1):
        route = record["route"]
        print(
            f"{i}. {record['source']} -> {record['destination']} | "
            f"Path: {' -> '.join(route.path)} | "
            f"Cost: {route.total_weight} | "
            f"Time: {record['timestamp']}"
        )


def show_menu():
    print("\n================ CAMPUS NAVIGATION & EVENT MANAGEMENT ================")
    print("1. Show buildings")
    print("2. Show pathways")
    print("3. Find shortest path")
    print("4. Undo last navigation")
    print("5. Show navigation history")
    print("6. Add booking")
    print("7. Remove booking")
    print("8. View bookings for a day")
    print("9. Query bookings by time range")
    print("10. Show next upcoming event")
    print("11. Add service request")
    print("12. Serve next service request")
    print("13. Lookup building")
    print("14. Lookup room")
    print("15. Delete building")
    print("16. Delete room")
    print("17. Enqueue incoming request")
    print("18. Process next incoming request")
    print("19. Auto-load 20 incoming requests")
    print("20. Run full demo mode")
    print("21. Exit")


def main():
    app = CampusNavigationApp()

    while True:
        show_menu()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            show_buildings(app)

        elif choice == "2":
            show_pathways(app)

        elif choice == "3":
            source_id = input("Enter source building ID: ").strip().upper()
            destination_id = input("Enter destination building ID: ").strip().upper()

            try:
                route = app.find_shortest_path(source_id, destination_id)
                print_route(route)
            except Exception as error:
                print(f"Error: {error}")

        elif choice == "4":
            success, current = app.undo_navigation()
            if success:
                print(f"Current location after undo: {current}")
            else:
                print("No navigation action to undo.")

        elif choice == "5":
            show_navigation_history(app)

        elif choice == "6":
            add_booking_menu(app)

        elif choice == "7":
            remove_booking_menu(app)

        elif choice == "8":
            date = input("Enter date (YYYY-MM-DD): ").strip()
            bookings = app.get_bookings_for_day(date)
            print_bookings(bookings, f"Bookings for {date}")

        elif choice == "9":
            date = input("Enter date (YYYY-MM-DD): ").strip()
            start = read_int("Start time in minutes from midnight: ", 0, 1439)
            end = read_int("End time in minutes from midnight: ", start + 1, 1440)
            bookings = app.get_bookings_in_time_range(date, start, end)
            print_bookings(
                bookings,
                f"Bookings on {date} between {format_minutes(start)} and {format_minutes(end)}",
            )

        elif choice == "10":
            booking = app.get_next_upcoming_event()
            print("\n--- Next Upcoming Event ---")
            if booking is None:
                print("No upcoming events.")
            else:
                print_booking(booking)

        elif choice == "11":
            add_service_request_menu(app)

        elif choice == "12":
            serve_next_service_request(app)

        elif choice == "13":
            lookup_building(app)

        elif choice == "14":
            lookup_room(app)

        elif choice == "15":
            delete_building_menu(app)

        elif choice == "16":
            delete_room_menu(app)

        elif choice == "17":
            enqueue_incoming_request_menu(app)

        elif choice == "18":
            process_next_incoming_request(app)

        elif choice == "19":
            simulate_request_pipeline(app)

        elif choice == "20":
            app.run_demo()

        elif choice == "21":
            print("Exiting application.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
