import requests
import time
import os

API_KEY = os.getenv("RAPIDAPI_KEY")

print("Flight Tracker Started")

while True:

    print("Checking API...")

    url = "https://sky-scrapper.p.rapidapi.com/api/v1/flights/searchAirport"

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "sky-scrapper.p.rapidapi.com"
    }

    params = {
        "query": "BOM"
    }

    r = requests.get(url,
                     headers=headers,
                     params=params)

    print("API Working")

    time.sleep(86400)
