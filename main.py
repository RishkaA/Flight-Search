from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

DEPARTURE_CITY_IATA = "LON"

# creating class objects 
data_manager = DataManager()
flightsearch = FlightSearch()
notification = NotificationManager()

# storing flight data in a new variable
sheet_data = data_manager.get_sheety_data()


def add_user():
  '''
  functions takes the details from the user and adds them to the sheet
  '''
  first_name = input("What is your first name? ").title()
  last_name = input("What is your last name? ").title()

  while True:
    email = input("What is your email address? ")
    email_confirm = input("Confirm your email address ")
    if email.lower() == email_confirm.lower():
      print("You're in the club!")
      break
    else:
      print("Emails don't match, pelase try again.")
  
  data_manager.add_user(first_name, last_name, email)


def search_flights():
  '''
  function is looking for flights to the destinations specified in google sheet 
  and sends sms and email notifications if flights meet the price proteria
  '''
  # if there is no iata code on the sheet, finding one usinf api and filling in the bank in   the google sheet
  if sheet_data[0]["iataCode"] == "":
      for row in sheet_data:
          row["iataCode"] = flightsearch.get_destination_code(row["city"])
      data_manager.destination_data = sheet_data
      data_manager.update_destination_codes()

  # determiting the from and to dates for the flight search
  tomorrow = datetime.now() + timedelta(days=1)
  in_six_months = tomorrow + timedelta(days=30*6)

  users = data_manager.get_sheety_users()
  
  for city in sheet_data:
      try:
        # looking for flights using variables determided above
          flight = flightsearch.find_flights(
              DEPARTURE_CITY_IATA,
              city["iataCode"],
              tomorrow,
              in_six_months
          )
          found_price = int(flight.price[0])
      except AttributeError:
        # if flight now found, continuing to the next city
          print(f"No flights found for {city['city']}")
          continue
      else:
        # if found price suits us based on te pre-determined price in the google sheet, sending me a message
        # and sending mails to all registered users with flight details
          if found_price <= city["lowestPrice"]:
              message_body = f"Low price alert! Only £{flight.price[0]} to fly from {flight.departure_city[0]}-{flight.departure_airport[0]} to {flight.to_city[0]}-{flight.to_airport[0]}, from {flight.from_date[0]} to {flight.to_date}."
              # sending myself an message
              message = notification.send_message(
                  message_body=message_body
              )
              # sending emails to users
              for user in users:
                  user_email = user["email"]
                  notification.send_email(user_email, message_body)
              # adding more info to message if flight has stopovers 
              if flight.outbound_stopovers[0] > 0:
                  message_body += f"{flight.outbound_stopovers[0]} stopover outbound via {flight.outbound_via_city[0]} {flight.back_stopovers[0]} stopover   returning via  {flight.back_via_city}"
                  message = notification.send_message(
                      message_body=message_body
                      )
                  for user in users:
                      user_email = user["email"]
                      notification.send_email(user_email, message_body)
  

add_user()
search_flights()
