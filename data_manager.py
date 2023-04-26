import requests
import os

BEARER = os.environ.get("BEARER")
USER = os.environ.get("SHEETY_USER")

SHEETY_URL = "https://api.sheety.co"

PROJECT_NAME = "flightDeals"
TAB_NAME = "price"

sheety_endpoint = f"{SHEETY_URL}/{USER}/{PROJECT_NAME}/{TAB_NAME}"

header = {
      "Authorization": f"Bearer {BEARER}",
      "Content-Type": "application/json",
    }

class DataManager:

    def __init__(self):
        self.destination_data = {}

    def get_sheety_data(self):
        response = requests.get(url=sheety_endpoint, headers=header)
        data = response.json()
        self.destination_data = data["price"]
        return self.destination_data

    def update_destination_codes(self):
      
      for row in self.destination_data:
          new_data = {
              "price": {
                  "iataCode": row["iataCode"]
              }
          }
          response = requests.put(
              url=f"{sheety_endpoint}/{row['id']}",
              headers=header,
              json=new_data
          )
          print(response.text)

