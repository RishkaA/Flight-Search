from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

DEPARTURE_CITY_IATA = "LON"

new_data = DataManager()
flightsearch = FlightSearch()
notification = NotificationManager()

sheet_data = new_data.get_sheety_data()

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flightsearch.get_destination_code(row["city"])
    new_data.destination_data = sheet_data
    new_data.update_destination_codes()

tomorrow = datetime.now() + timedelta(days=1)
in_six_months = tomorrow + timedelta(days=30*6)

for city in sheet_data:
    flight = flightsearch.find_flights(
        DEPARTURE_CITY_IATA,
        city["iataCode"],
        tomorrow,
        in_six_months
    )
    new_price = int(flight.price[0])
    if new_price <= city["lowestPrice"]:
        message = notification.send_message(
            message_body=f"Low price alert! Only £{flight.price[0]} "
                         f"to fly from {flight.departure_city[0]}-{flight.departure_airport[0]} "
                         f"to {flight.to_city[0]}-{flight.to_airport[0]}, "
                         f"from {flight.from_date[0]} to {flight.to_date}."
            )





