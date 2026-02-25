import requests
import os
import csv
from datetime import datetime

API_KEY = os.getenv("RAPIDAPI_KEY")

ORIGIN = "BOM"
DESTINATION = "DEL"
DATE = "2026-03-10"

CSV_FILE = "prices.csv"

HOST = "sky-scrapper.p.rapidapi.com"


def get_airport_id(code):

    try:

        url = "https://sky-scrapper.p.rapidapi.com/api/v1/flights/searchAirport"

        headers = {
            "x-rapidapi-key": API_KEY,
            "x-rapidapi-host": HOST
        }

        r = requests.get(url, headers=headers, params={"query": code})

        data = r.json()

        return data["data"][0]["entityId"]

    except:

        print("Airport lookup failed")

        return None


def get_price(origin_id, dest_id):

    try:

        url = "https://sky-scrapper.p.rapidapi.com/api/v1/flights/searchFlights"

        headers = {
            "x-rapidapi-key": API_KEY,
            "x-rapidapi-host": HOST
        }

        params = {

            "originSkyId": ORIGIN,
            "destinationSkyId": DESTINATION,

            "originEntityId": origin_id,
            "destinationEntityId": dest_id,

            "date": DATE,

            "adults": 1,
            "currency": "INR"
        }

        r = requests.get(url, headers=headers, params=params)

        data = r.json()

        if "data" not in data:

            print("No API data")
            return None

        itineraries = data["data"].get("itineraries", [])

        if len(itineraries) == 0:

            print("No flights found")
            return None

        return itineraries[0]["price"]["raw"]

    except:

        print("Price lookup failed")

        return None


def save_price(price):

    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, "a", newline="") as f:

        writer = csv.writer(f)

        if not file_exists:

            writer.writerow(["DateTime", "Price"])

        writer.writerow([datetime.now(), price])


print("Starting Flight Tracker")

origin_id = get_airport_id(ORIGIN)
dest_id = get_airport_id(DESTINATION)

if origin_id and dest_id:

    price = get_price(origin_id, dest_id)

    if price:

        print("Price =", price)

        save_price(price)

    else:

        print("Price not found")

else:

    print("Airport error")

print("Finished")
