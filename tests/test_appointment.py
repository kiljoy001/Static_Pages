"""
This module contains tests for module appointment.

"""
import unittest
from datetime import datetime
from src.appointment import Appointment

class TestAppointment(unittest.TestCase):
    def test_appointment_can_return_correct_date(self) -> None:
        """
        tests if the appointment can return correct date
        @param self:
        @return:
        """
        # Arrange
        date = datetime.now()
        event_name = "Test Contact"
        phone_number = "+155555555"
        location = "Location 1"
        lead_message = "Interested in your services"

        # Act
        test_appointment = Appointment(date, event_name, phone_number, location, lead_message)

        # Assert
        assert test_appointment.date == date

    def test_appointment_returns_correct_event_name(self) -> None:
        """
        Tests if the appointment can return correct event name
        @param self:
        @return:
        """

        # Arrange
        date = datetime.now()
        event_name = "Test Contact"
        phone_number = "+155555555"
        location = "Location 1"
        lead_message = "Interested in your services"

        # Act
        test_appointment = Appointment(date, event_name, phone_number, location, lead_message)

        # Assert
        assert test_appointment.event_name == event_name

    def test_appointment_returns_correct_phone_number(self) -> None:
        """
        Tests if the appointment can return correct phone number
        @param self:
        @return:
        """
        # Arrange
        date = datetime.now()
        event_name = "Test Contact"
        phone_number = "+155555555"
        location = "Location 1"
        lead_message = "Interested in your services"

        # Act
        test_appointment = Appointment(date, event_name, phone_number, location, lead_message)

        # Assert
        assert test_appointment.phone_number == phone_number

    def test_appointment_returns_correct_location(self) -> None:
        """
        Tests if the appointment can return correct location
        @param self:
        @return:
        """

        # Arrange
        date = datetime.now()
        event_name = "Test Contact"
        phone_number = "+155555555"
        location = "Location 1"
        lead_message = "Interested in your services"

        # Act
        test_appointment = Appointment(date, event_name, phone_number, location, lead_message)

        # Assert
        assert test_appointment.location == location

    def test_appointment_returns_correct_message(self) -> None:

        # Arrange
        date = datetime.now()
        event_name = "Test Contact"
        phone_number = "+155555555"
        location = "Location 1"
        lead_message = "Interested in your services"

        # Act
        test_appointment = Appointment(date, event_name, phone_number, location, lead_message)

        # Assert
        assert test_appointment.message == lead_message
