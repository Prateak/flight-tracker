import requests
import os
import csv
from datetime import datetime, timedelta

API_KEY = os.getenv("RAPIDAPI_KEY")

ORIGIN = "BOM"
DESTINATION = "DEL"

CSV_FILE = "prices.csv"

HOST = "sky-scrapper.p.rapidapi.com"


def get_airport_id(code):

    url = "https://sky-scrapper.p.rapidapi.com/api/v1/flights/searchAirport"

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": HOST
    }

    r = requests.get(url, headers=headers, params={"query": code})

    data = r.json()

    return data["data"][0]["entityId"]


def find_flight(origin_id, dest_id):

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": HOST
    }

    for i in range(1,20):

        date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")

        print("Checking:", date)

        params = {

            "originSkyId": ORIGIN,
            "destinationSkyId": DESTINATION,

            "originEntityId": origin_id,
            "destinationEntityId": dest_id,

            "date": date,

            "adults": 1,
            "currency": "INR"
        }

        url = "https://sky-scrapper.p.rapidapi.com/api/v1/flights/searchFlights"

        r = requests.get(url, headers=headers, params=params)

        data = r.json()

        if "data" not in data:
            continue

        itineraries = data["data"].get("itineraries", [])

        if len(itineraries) == 0:
            continue

        try:

            flight = itineraries[0]

            leg = flight["legs"][0]

            segment = leg["segments"][0]

            carrier = segment["marketingCarrier"]["alternateId"]

            number = segment["flightNumber"]

            flight_number = carrier + number

            departure = leg.get("departure","NA")

            arrival = leg.get("arrival","NA")

            price = flight["price"]["raw"]

            return date, flight_number, departure, arrival, price

        except:

            continue

    return "NA","NA","NA","NA","NA"


def save_data(date, flight_number, departure, arrival, price):

    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, "a", newline="") as f:

        writer = csv.writer(f)

        if not file_exists:

            writer.writerow([
                "CheckedOn",
                "FlightDate",
                "FlightNumber",
                "Departure",
                "Arrival",
                "Price"
            ])

        writer.writerow([
            datetime.now(),
            date,
            flight_number,
            departure,
            arrival,
            price
        ])


print("Starting Tracker")

origin_id = get_airport_id(ORIGIN)
dest_id = get_airport_id(DESTINATION)

date, flight_number, departure, arrival, price = find_flight(origin_id, dest_id)

print("Flight:",flight_number)
print("Price:",price)

save_data(date, flight_number, departure, arrival, price)

print("CSV Saved")
