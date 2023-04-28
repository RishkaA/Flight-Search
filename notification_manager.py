import os
from twilio.rest import Client
import smtplib

TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_TOKEN = os.environ.get("TWILIO_TOKEN")
TWILIO_FROM = os.environ.get("FROM_NUMBER")
TWILIO_TO = os.environ.get("TO_NUMBER")

MY_EMAIL = my_email
MY_PASSWORD = my_password

class NotificationManager:
  '''
  class maages all notifications sent to the users

  methods:
    send_message(self, message_body):
      sends a text message using twilio api taking a message body as a parameter

    send_email(self, email_address, message):
      sends an email using smtplib taking email address and a message body as a parameter
  '''
  def __init__(self):
    
      self.client = Client(TWILIO_SID, TWILIO_TOKEN)

  def send_message(self, message_body):

      message = self.client.messages.create(
          from_= TWILIO_FROM,
          body=message_body,
          to= TWILIO_TO
      )

      print(message.sid)

  def send_email(self, email_address, message):

      connection = smtplib.SMTP("smtp.office365.com")
      connection.starttls()
      connection.login(MY_EMAIL, MY_PASSWORD)
      connection.sendmail(
          from_addr=MY_EMAIL,
          to_addrs=email_address,
          msg=message.encode("utf-8")
          )
  


