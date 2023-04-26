import requests

SHEETY_ENDPOINT = "https://api.sheety.co/fa42f62de5a8f220dff9fafa72f746e5/flightDeals/sheet1"

class DataManager:

    def __init__(self):
        self.destination_data = {}

    def get_sheety_data(self):
        response = requests.get(url=SHEETY_ENDPOINT)
        data = response.json()
        self.destination_data = data["sheet1"]
        return self.destination_data

    def update_destination_codes(self):
        for row in self.destination_data:
            new_data = {
                "sheet1": {
                    "iataCode": row["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_ENDPOINT}/{row['id']}",
                json=new_data
            )
            print(response.text)
