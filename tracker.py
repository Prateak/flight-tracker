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

    url = "https://sky-scrapper.p.rapidapi.com/api/v1/flights/searchAirport"

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": HOST
    }

    r = requests.get(url, headers=headers, params={"query": code})

    data = r.json()

    return data["data"][0]["entityId"]


def get_price(origin_id, dest_id):

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

        print("No data returned")
        return None

    itineraries = data["data"]["itineraries"]

    if len(itineraries) == 0:

        print("No flights found")
        return None

    price = itineraries[0]["price"]["raw"]

    return price


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

price = get_price(origin_id, dest_id)

if price:

    print("Price =", price)

    save_price(price)

else:

    print("Price not found")

print("Finished")
