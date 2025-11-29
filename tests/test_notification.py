
import unittest
from unittest.mock import patch, MagicMock
from src.notification import NotificationService

class TestNotificationService(unittest.TestCase):

    @patch('src.notification.os.environ.get')
    @patch('src.notification.Client')
    def test_send_sms_success(self, mock_client, mock_env):
        # Setup
        def get_env_side_effect(key, default=None):
            if key == "TWILIO_ACCOUNT_SID": return "AC123"
            if key == "TWILIO_AUTH_TOKEN": return "token"
            if key == "TWILIO_PHONE_NUMBER": return "+1234567890"
            return default
        mock_env.side_effect = get_env_side_effect

        mock_messages = MagicMock()
        mock_client.return_value.messages = mock_messages
        mock_messages.create.return_value.sid = "SM123"

        service = NotificationService()

        # Act
        result = service.send_sms("+0987654321", "Test Message")

        # Assert
        self.assertTrue(result)
        mock_messages.create.assert_called_once_with(
            body="Test Message",
            from_="+1234567890",
            to="+0987654321"
        )

    @patch('src.notification.os.environ.get')
    @patch('src.notification.Client')
    def test_make_call_success(self, mock_client, mock_env):
        # Setup
        def get_env_side_effect(key, default=None):
            if key == "TWILIO_ACCOUNT_SID": return "AC123"
            if key == "TWILIO_AUTH_TOKEN": return "token"
            if key == "TWILIO_PHONE_NUMBER": return "+1234567890"
            return default
        mock_env.side_effect = get_env_side_effect

        mock_calls = MagicMock()
        mock_client.return_value.calls = mock_calls
        mock_calls.create.return_value.sid = "CA123"

        service = NotificationService()

        # Act
        result = service.make_call("+0987654321", "Test Message")

        # Assert
        self.assertTrue(result)
        mock_calls.create.assert_called_once_with(
            twiml="<Response><Say>Test Message</Say></Response>",
            from_="+1234567890",
            to="+0987654321"
        )

    @patch('src.notification.SendGridAPIClient')
    def test_send_email_success(self, mock_sg_client):
        # Setup
        mock_sg_instance = MagicMock()
        mock_sg_client.return_value = mock_sg_instance
        mock_sg_instance.send.return_value.status_code = 202

        service = NotificationService()
        service.sendgrid_api_key = "SG.123"

        # Act
        result = service.send_email("test@example.com", "Subject", "Content")

        # Assert
        self.assertTrue(result)
        mock_sg_instance.send.assert_called_once()
