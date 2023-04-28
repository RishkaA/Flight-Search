class FlightData:
  '''
  class stores iformation of one flight found in the search
  '''
  def __init__(self, price, departure_airport, departure_city, to_airport, to_city, from_date, to_date, outbound_stopovers=0, back_stopovers=0,  outbound_via_city="", back_via_city=""):
     self.price = price,
     self.departure_airport = departure_airport,
     self.departure_city = departure_city,
     self.to_airport = to_airport,
     self.to_city = to_city,
     self.from_date = from_date,
     self.to_date = to_date
     self.outbound_stopovers = outbound_stopovers,
     self.back_stopovers = back_stopovers,
     self.outbound_via_city = outbound_via_city,
     self.back_via_city = back_via_city
