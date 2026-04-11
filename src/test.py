from Booking_system import BookingSystem
from models import Booking


def run_booking_tests():
    bs = BookingSystem()

    b1 = Booking("B1", "ICT-121", "Math Lecture", "2026-04-15", 600, 660, "Prof A")
    b2 = Booking("B2", "ICT-121", "Study Group", "2026-04-15", 700, 760, "Student Club")
    b3 = Booking("B3", "ICT-121", "Conflicting Event", "2026-04-15", 650, 720, "Someone")

    print("Add B1:", bs.add_booking(b1))   # True
    print("Add B2:", bs.add_booking(b2))   # True
    print("Add B3 (should fail):", bs.add_booking(b3))   # False

    print("\nBookings for day:")
    for b in bs.get_bookings_for_day("2026-04-15"):
        print(b.event_title)

    print("\nBookings in time range 590–710:")
    for b in bs.get_bookings_in_time_range("2026-04-15", 590, 710):
        print(b.event_title)

    print("\nRemove B1:", bs.remove_booking("B1"))

    next_event = bs.get_next_upcoming_event()
    if next_event:
        print("Next event:", next_event.event_title)
    else:
        print("No upcoming events")


if __name__ == "__main__":
    run_booking_tests()