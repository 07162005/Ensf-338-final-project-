from models import Booking


class BookingSystem:
    def __init__(self):
        self.all_bookings = []   # list of Booking objects

    def add_booking(self, booking: Booking):
        # Check for conflict
        if self.has_conflict(booking):
            print("Booking conflict detected!")
            return False

        # Add booking
        self.all_bookings.append(booking)

        # Keep sorted by date + start time
        self.all_bookings.sort(key=lambda b: (b.event_date, b.start_time))

        return True

    def remove_booking(self, booking_id: str):
        for b in self.all_bookings:
            if b.booking_id == booking_id:
                self.all_bookings.remove(b)
                return True
        return False

    def get_bookings_for_day(self, event_date: str):
        result = []
        for b in self.all_bookings:
            if b.event_date == event_date:
                result.append(b)
        return result

    def get_bookings_in_time_range(self, event_date: str, start_time: int, end_time: int):
        result = []
        for b in self.all_bookings:
            if b.event_date == event_date:
                # Check overlap
                if not (b.end_time <= start_time or b.start_time >= end_time):
                    result.append(b)
        return result

    def get_next_upcoming_event(self):
        if len(self.all_bookings) == 0:
            return None
        return self.all_bookings[0]

    def has_conflict(self, new_booking: Booking):
        for b in self.all_bookings:
            if b.room_id == new_booking.room_id and b.event_date == new_booking.event_date:
                # Check time overlap
                if not (new_booking.end_time <= b.start_time or new_booking.start_time >= b.end_time):
                    return True
        return False