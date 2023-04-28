import os
import requests
from flight_data import FlightData

kiwi_flight_api = os.environ.get("KIWI_FLIGHT_API")
kiwi_endpoint = "https://api.tequila.kiwi.com"


class FlightSearch:
  '''
  class is used for all the actions that are required to lookup flights

  methods:
    get_destination_code(self, city):
      method gets the aita code for the city that is passed as a parameter
      using tequila location api

    find_flights(self, origin_city_code, destination_city_code, from_time, to_time):
      method uses tequila search api to find cheapest flights using destination and dates
      parameters passed by the user
  '''

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
    # getting a code from the returned result
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
          print(f"{data['cityTo']}: £{data['price']}")
    except IndexError:
          # if no flights found, changing the max_stopovers parameter
          parameters["max_stopovers"] = 2
          response = requests.get(url=f"{kiwi_endpoint}/v2/search",
                                  headers=header,
                                  params=parameters)

          data = response.json()["data"][0]

          # calculating the amount of flights each way (outbund and return)
          # to later determine the amount of stopovers
          outbound_flights = 0
          back_flights = 0
          for flight in data["route"]:
              if flight['return'] == 0:
                  outbound_flights += 1
              elif flight['return'] == 1:
                  back_flights += 1

          # recording stopover data for the flight
          flightdata = FlightData(
              price=data["price"],
              departure_city=data["route"][0]["cityFrom"],
              departure_airport=data["route"][0]["flyFrom"],
              to_city=data["route"][1]["cityTo"],
              to_airport=data["route"][1]["flyTo"],
              from_date=data["route"][0]["local_departure"].split("T")[0],
              to_date=data["route"][2]["local_departure"].split("T")[0],
              outbound_stopovers=outbound_flights - 1,
              back_stopovers=back_flights - 1,
              outbound_via_city=data["route"][0]["cityTo"],
              back_via_city=data["route"][-1]["cityFrom"]
          )

          return flightdata
    else:
          # no stopover data recorded for direct flight
          flightdata = FlightData(
              price=data["price"],
              departure_city= data["route"][0]["cityFrom"],
              departure_airport=data["route"][0]["flyFrom"],
              to_city=data["route"][0]["cityTo"],
              to_airport=data["route"][0]["flyTo"],
              from_date=data["route"][0]["local_departure"].split("T")[0],
              to_date=data["route"][0]["local_arrival"].split("T")[0]
          )

    return flightdata
