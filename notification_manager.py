import os
from twilio.rest import Client

TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_TOKEN = os.environ.get("TWILIO_TOKEN")
TWILIO_FROM = os.environ.get("FROM_NUMBER")
TWILIO_TO = os.environ.get("TO_NUMBER")

class NotificationManager:

    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_TOKEN)

    def send_message(self, message_body):

        message = self.client.messages.create(
            from_= TWILIO_FROM,
            body=message_body,
            to= TWILIO_TO
        )

        print(message.sid)

