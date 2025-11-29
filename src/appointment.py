from datetime import datetime

class Appointment:
    def __init__(self, date: datetime, event_name: str, phone_number: str, location: str, message: str):
        self.date = date
        self.event_name = event_name
        self.phone_number = phone_number
        self.location = location
        self.message = message

    def __eq__(self, other):
        if not isinstance(other, Appointment):
            return False
        return (self.date == other.date and
                self.event_name == other.event_name and
                self.phone_number == other.phone_number and
                self.location == other.location and
                self.message == other.message)
