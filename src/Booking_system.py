from models import Booking


class BookingSystem:
    def __init__(self):
        self.all_bookings = []   # list of Booking objects
                                 # You may later replace this with a BST/AVL structure

    def add_booking(self, booking: Booking):
        # TODO:
        # 1. Check if booking conflicts with an existing booking for same room/date/time
        # 2. If no conflict, add to all_bookings
        # 3. Keep ordered if you want easier retrieval
        pass

    def remove_booking(self, booking_id: str):
        # TODO:
        # Remove booking with matching booking_id
        pass

    def get_bookings_for_day(self, event_date: str):
        # TODO:
        # Return all bookings on the given date
        pass

    def get_bookings_in_time_range(self, event_date: str, start_time: int, end_time: int):
        # TODO:
        # Return all bookings overlapping the given time range
        pass

    def get_next_upcoming_event(self):
        # TODO:
        # Return next upcoming booking in sorted order
        pass

    def has_conflict(self, new_booking: Booking):
        # TODO:
        # Check overlap against bookings in same room and same date
        pass