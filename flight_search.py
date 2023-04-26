import os
import requests
from flight_data import FlightData

kiwi_flight_api = os.environ.get("KIWI_FLIGHT_API")
kiwi_endpoint = "https://api.tequila.kiwi.com"


class FlightSearch:

    def get_destination_code(self, city):
       header = {
           "apikey": kiwi_flight_api
       }

       parameters = {
           "term": city,
           "location_types": "city"
       }
       response = requests.get(url=f"{kiwi_endpoint}/locations/query",
                           headers=header,
                           params=parameters)
       results = response.json()["locations"]
       code = results[0]["code"]
       return code

    def find_flights(self, origin_city_code, destination_city_code, from_time, to_time):

        header = {
           "apikey": kiwi_flight_api
       }

        parameters = {
           "fly_from": origin_city_code,
           "fly_to": destination_city_code,
           "date_from": from_time.strftime("%d/%m/%Y"),
           "date_to": to_time.strftime("%d/%m/%Y"),
           "nights_in_dst_from": 7,
           "nights_in_dst_to": 28,
           "flight_type": "round",
           "one_for_city": 1,
           "curr": "GBP",
           "max_stopovers": 0,
       }

        response = requests.get(url=f"{kiwi_endpoint}/v2/search",
                               headers=header,
                               params=parameters)

        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {destination_city_code}.")
            return None

        flightdata = FlightData(
            price=data["price"],
            departure_city= data["route"][0]["cityFrom"],
            departure_airport=data["route"][0]["flyFrom"],
            to_city=data["route"][0]["cityTo"],
            to_airport=data["route"][0]["flyTo"],
            from_date=data["route"][0]["local_departure"].split("T")[0],
            to_date=data["route"][0]["local_arrival"].split("T")[0]
        )

        print(f"{flightdata.to_city[0]}: £{flightdata.price[0]}")
        return flightdata




