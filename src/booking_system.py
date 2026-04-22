class BookingSystem:
    def __init__(self):
        self.bookings = []
        self.count = 0

    def add_booking(self, booking):
        if self.has_conflict(booking):
            return False

        self.bookings.append(booking)
        self.bookings.sort(key=lambda b: (b.event_date, b.start_time, b.booking_id))
        self.count += 1
        return True

    def remove_booking(self, booking_id: str):
        for i, booking in enumerate(self.bookings):
            if booking.booking_id == booking_id:
                self.bookings.pop(i)
                self.count -= 1
                return True
        return False

    def get_bookings_for_day(self, event_date: str):
        results = []
        for booking in self.bookings:
            if booking.event_date == event_date:
                results.append(booking)
        return results

    def get_bookings_in_time_range(self, event_date: str, start_time: int, end_time: int):
        results = []
        for booking in self.bookings:
            same_day = booking.event_date == event_date
            overlaps = booking.start_time < end_time and booking.end_time > start_time
            if same_day and overlaps:
                results.append(booking)
        return results

    def get_next_upcoming_event(self):
        if len(self.bookings) == 0:
            return None
        return self.bookings[0]

    def has_conflict(self, new_booking):
        for booking in self.bookings:
            same_room = booking.room_id == new_booking.room_id
            same_day = booking.event_date == new_booking.event_date
            overlap = booking.start_time < new_booking.end_time and booking.end_time > new_booking.start_time
            if same_room and same_day and overlap:
                return True
        return False