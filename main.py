import os
from Demo import build_demo_system
from navigation import NavigationManager
from models import NavigationSession, Booking, Building, Room
from lookup import LookupManager
from HelperFunctions import time_to_minutes, minutes_to_time, validate_date, format_route

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def print_menu():
    print("\n=== Campus Navigation and Event Management System ===")
    print("1. Show buildings")
    print("2. Find shortest path")
    print("3. Undo last navigation")
    print("4. Show bookings for a day")
    print("5. Show bookings in a time range")
    print("6. Add booking")
    print("7. Remove booking")
    print("8. Show next service request")
    print("9. Serve next service request")
    print("10. Show next incoming request")
    print("11. Process next incoming request")
    print("12. Lookup building by ID")
    print("13. Lookup room by ID")
    print("14. Add building")
    print("15. Add room")
    print("16. Delete building")
    print("17. Delete room")
    print("18. Run quick demo")
    print("0. Exit")


def show_buildings(campus):
    building_list = campus.buildings.values()
    building_list.sort(key=lambda b: b.building_id)

    for building in building_list:
        print(f"{building.building_id} - {building.name} ({len(building.rooms.keys())} rooms)")


def show_bookings(bookings):
    if len(bookings) == 0:
        print("No bookings found.")
        return

    for booking in bookings:
        print(
            f"{booking.booking_id} | {booking.room_id} | {booking.event_title} | "
            f"{booking.event_date} | {minutes_to_time(booking.start_time)}-"
            f"{minutes_to_time(booking.end_time)} | {booking.organizer}"
        )


def run_quick_demo(campus, navigation_manager, session, booking_system, priority_queue, request_queue):
    print("\n--- Quick Demo ---")

    route = navigation_manager.navigate(session, "ICT", "HNSC")
    if route is not None:
        print(format_route(route))

    undone = navigation_manager.undo_last_navigation(session)
    if undone is not None:
        print(f"Undid route: {undone.source_id} -> {undone.destination_id}")

    print("\nBookings on 2026-04-20:")
    show_bookings(booking_system.get_bookings_for_day("2026-04-20"))

    print("\nNext service request:")
    service = priority_queue.peek()
    if service is not None:
        print(f"{service.request_id} | {service.service_type} | priority {service.priority}")

    print("\nProcessing first three incoming requests:")
    for _ in range(3):
        request = request_queue.dequeue()
        if request is not None:
            print(f"Processed {request.request_id} | {request.request_type} | {request.payload}")


def main():
    campus, graph, booking_system, priority_queue, request_queue = build_demo_system(DATA_DIR)
    navigation_manager = NavigationManager(graph)
    lookup_manager = LookupManager(campus)
    session = NavigationSession("demo_user")
    booking_counter = booking_system.count + 1

    while True:
        print_menu()
        choice = input("Select an option: ").strip()

        if choice == "1":
            show_buildings(campus)

        elif choice == "2":
            source = input("Source building ID: ").strip().upper()
            destination = input("Destination building ID: ").strip().upper()
            route = navigation_manager.navigate(session, source, destination)

            if route is None:
                print("No route found.")
            else:
                print(format_route(route))

        elif choice == "3":
            route = navigation_manager.undo_last_navigation(session)

            if route is None:
                print("No route to undo.")
            else:
                print(f"Undid route: {route.source_id} -> {route.destination_id}")
                print(f"Current location: {session.current_location}")

        elif choice == "4":
            date = input("Date (YYYY-MM-DD): ").strip()

            if not validate_date(date):
                print("Invalid date.")
            else:
                show_bookings(booking_system.get_bookings_for_day(date))

        elif choice == "5":
            date = input("Date (YYYY-MM-DD): ").strip()
            start = input("Start time (HH:MM): ").strip()
            end = input("End time (HH:MM): ").strip()

            if not validate_date(date):
                print("Invalid date.")
            else:
                bookings = booking_system.get_bookings_in_time_range(
                    date, time_to_minutes(start), time_to_minutes(end)
                )
                show_bookings(bookings)

        elif choice == "6":
            room_id = input("Room ID: ").strip().upper()
            title = input("Event title: ").strip()
            date = input("Date (YYYY-MM-DD): ").strip()
            start = input("Start time (HH:MM): ").strip()
            end = input("End time (HH:MM): ").strip()
            organizer = input("Organizer: ").strip()

            booking = Booking(
                f"BK{booking_counter:03d}",
                room_id,
                title,
                date,
                time_to_minutes(start),
                time_to_minutes(end),
                organizer,
            )

            if booking_system.add_booking(booking):
                booking_counter += 1
                print("Booking added.")
            else:
                print("Booking conflicts with an existing booking.")

        elif choice == "7":
            booking_id = input("Booking ID: ").strip().upper()

            if booking_system.remove_booking(booking_id):
                print("Booking removed.")
            else:
                print("Booking not found.")

        elif choice == "8":
            request = priority_queue.peek()

            if request is None:
                print("No service requests.")
            else:
                print(f"{request.request_id} | {request.requester_name} | {request.service_type} | priority {request.priority}")

        elif choice == "9":
            request = priority_queue.serve_next()

            if request is None:
                print("No service requests.")
            else:
                print(f"Served {request.request_id} ({request.service_type})")

        elif choice == "10":
            request = request_queue.peek()

            if request is None:
                print("No incoming requests.")
            else:
                print(f"Next: {request.request_id} | {request.request_type} | {request.payload}")

        elif choice == "11":
            request = request_queue.dequeue()

            if request is None:
                print("No incoming requests.")
            else:
                print(f"Processed {request.request_id} | {request.request_type} | {request.payload}")

        elif choice == "12":
            building_id = input("Building ID: ").strip().upper()
            building = lookup_manager.lookup_building(building_id)

            if building is None:
                print("Building not found.")
            else:
                print(f"Building ID: {building.building_id}")
                print(f"Name: {building.name}")
                print(f"Location: {building.location}")
                print(f"Number of rooms: {len(building.rooms.keys())}")

        elif choice == "13":
            building_id = input("Building ID: ").strip().upper()
            room_id = input("Room ID: ").strip().upper()
            room = lookup_manager.lookup_room(building_id, room_id)

            if room is None:
                print("Room not found.")
            else:
                print(f"Room ID: {room.room_id}")
                print(f"Capacity: {room.capacity}")
                print(f"Type: {room.room_type}")
                print(f"Bookings: {len(room.bookings)}")

        elif choice == "14":
            building_id = input("New building ID: ").strip().upper()
            name = input("Building name: ").strip()
            x = float(input("Location x: ").strip())
            y = float(input("Location y: ").strip())

            building = Building(building_id, name, (x, y))
            lookup_manager.insert_building(building)
            print("Building added.")

        elif choice == "15":
            building_id = input("Building ID: ").strip().upper()
            room_id = input("New room ID: ").strip().upper()
            capacity = int(input("Capacity: ").strip())
            room_type = input("Room type: ").strip().lower()

            room = Room(room_id, capacity, room_type)

            if lookup_manager.insert_room(building_id, room):
                print("Room added.")
            else:
                print("Building not found.")

        elif choice == "16":
            building_id = input("Building ID to delete: ").strip().upper()

            if lookup_manager.delete_building(building_id):
                print("Building deleted.")
            else:
                print("Building not found.")

        elif choice == "17":
            building_id = input("Building ID: ").strip().upper()
            room_id = input("Room ID to delete: ").strip().upper()

            if lookup_manager.delete_room(building_id, room_id):
                print("Room deleted.")
            else:
                print("Room not found.")

        elif choice == "18":
            run_quick_demo(campus, navigation_manager, session, booking_system, priority_queue, request_queue)

        elif choice == "0":
            print("Goodbye.")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()