import os
from twilio.rest import Client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class NotificationService:
    def __init__(self):
        self.twilio_account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        self.twilio_auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        self.twilio_phone_number = os.environ.get("TWILIO_PHONE_NUMBER")
        self.sendgrid_api_key = os.environ.get("SENDGRID_API_KEY")
        self.sendgrid_from_email = os.environ.get("SENDGRID_FROM_EMAIL", "noreply@example.com")

        if self.twilio_account_sid and self.twilio_auth_token:
            self.twilio_client = Client(self.twilio_account_sid, self.twilio_auth_token)
        else:
            self.twilio_client = None
            print("Twilio credentials not found.")

    def send_sms(self, to_number: str, body: str) -> bool:
        if not self.twilio_client or not self.twilio_phone_number:
            print("Twilio client not initialized or phone number missing.")
            return False
        try:
            message = self.twilio_client.messages.create(
                body=body,
                from_=self.twilio_phone_number,
                to=to_number
            )
            print(f"SMS sent: {message.sid}")
            return True
        except Exception as e:
            print(f"Failed to send SMS: {e}")
            return False

    def make_call(self, to_number: str, message: str) -> bool:
        if not self.twilio_client or not self.twilio_phone_number:
            print("Twilio client not initialized or phone number missing.")
            return False
        try:
            # TwiML to say the message
            twiml = f"<Response><Say>{message}</Say></Response>"
            call = self.twilio_client.calls.create(
                twiml=twiml,
                to=to_number,
                from_=self.twilio_phone_number
            )
            print(f"Call initiated: {call.sid}")
            return True
        except Exception as e:
            print(f"Failed to make call: {e}")
            return False

    def send_email(self, to_email: str, subject: str, content: str) -> bool:
        if not self.sendgrid_api_key:
            print("SendGrid API key not found.")
            return False
        try:
            message = Mail(
                from_email=self.sendgrid_from_email,
                to_emails=to_email,
                subject=subject,
                html_content=content
            )
            sg = SendGridAPIClient(self.sendgrid_api_key)
            response = sg.send(message)
            print(f"Email sent: {response.status_code}")
            return response.status_code in [200, 201, 202]
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
