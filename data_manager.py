import requests
import os

BEARER = os.environ.get("BEARER")
USER = os.environ.get("SHEETY_USER")

SHEETY_URL = "https://api.sheety.co"

PROJECT_NAME = "flightDeals"
PRICE_TAB_NAME = "price"
USERS_TAB_NAME = "users"

header = {
      "Authorization": f"Bearer {BEARER}",
      "Content-Type": "application/json",
    }

class DataManager:
  '''
  DataManager class manages the google sheet data using sheety api

  methods:
    get_sheety_data(self):
      collects all information about the fights from the 'price' tab in the google sheet

    get_sheety_users(self):
      collects all information about the registered users from the 'price' tab in the google sheet

    update_destination_codes(self):
      updates IATA codes in the price tab of the google sheet

    add_user(self, first_name, last_name, email):
      adds user to users tab of google sheet using detais passed as parameters
  '''

  def __init__(self):
      self.destination_data = {}
      self.users_data = {}

  def get_sheety_data(self):
      sheety_endpoint = f"{SHEETY_URL}/{USER}/{PROJECT_NAME}/{PRICE_TAB_NAME}"
      response = requests.get(url=sheety_endpoint, headers=header)
      data = response.json()
      self.destination_data = data["price"]
    
      return self.destination_data

  def get_sheety_users(self):
      sheety_endpoint = f"{SHEETY_URL}/{USER}/{PROJECT_NAME}/{USERS_TAB_NAME}"
      response = requests.get(url=sheety_endpoint, headers=header)
      data = response.json()
      self.users_data = data["users"]
    
      return self.users_data

  def update_destination_codes(self):
    
    for row in self.destination_data:
      sheety_endpoint = f"{SHEETY_URL}/{USER}/{PROJECT_NAME}/{PRICE_TAB_NAME}"
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

  def add_user(self, first_name, last_name, email):

    SHEETY_ENDPOINT = f"{SHEETY_URL}/{USER}/{PROJECT_NAME}/{USERS_TAB_NAME}"

    header = {
      "Authorization": f"Bearer {BEARER}",
      "Content-Type": "application/json",
    }
    
    parameters = {
      "user": {
        "firstName": first_name,
        "lastName": last_name,
        "email": email
          }
    }

    response = requests.post(url=SHEETY_ENDPOINT, headers=header, json=parameters)
    response.raise_for_status()
    print(response.text)
