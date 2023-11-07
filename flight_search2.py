import requests
from datetime import datetime, timedelta
from flight_data import FlightData

TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com"
TEQUILA_API_KEY = "placeholder"
TEQUILA_header = {
    "apikey": TEQUILA_API_KEY,
    "Content-Type": "application/json",
}
tomorrow = datetime.now() + timedelta(days=1)
time_interval = tomorrow + timedelta(days=180)


class FlightSearch:

    def get_flights(self, honnan, hova):
        search_params = {
            "fly_from": honnan,
            "fly_to": hova,
            "date_from": tomorrow.strftime("%d/%m/%Y"),
            "date_to": time_interval.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 4,
            "nights_in_dst_to": 5,
            "flight_type": "round",
            "curr": "huf",
            "one_for_city": 0,
            "max_stopovers": 1,
            "adults": 2,
            "limit": 3
        }
        response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", headers=TEQUILA_header,    params=search_params)
        response.raise_for_status()
        flights = []
        try:
            data = response.json()["data"]
        except IndexError:
            print(f"No direct flights found for {hova}.")
            search_params["max_stopovers"] = 1
            response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", headers=TEQUILA_header, params=search_params)
            response.raise_for_status()
            data = response.json()["data"]
            for result in data:
                flight = FlightData(
                    price=round(result["price"]),
                    origin_city=result["route"][0]["cityFrom"],
                    origin_airport=result["route"][0]["flyFrom"],
                    destination_city=result["route"][0]["cityTo"],
                    destination_airport=result["route"][0]["flyTo"],
                    out_date=result["route"][0]["local_departure"].split("T")[0],
                    return_date=result["route"][1]["local_departure"].split("T")[0],
                    out_airline=result["route"][0]["airline"],
                    return_airline=result["route"][1]["airline"],
                    link=result["deep_link"],
                    via_city=data["route"][0]["cityTo"],
                    stop_overs=1
                )
                flights.append(flight)
            return flights
        else:
            for result in data:
                flight = FlightData(
                    price=round(result["price"]),
                    origin_city=result["route"][0]["cityFrom"],
                    origin_airport=result["route"][0]["flyFrom"],
                    destination_city=result["route"][0]["cityTo"],
                    destination_airport=result["route"][0]["flyTo"],
                    out_date=result["route"][0]["local_departure"].split("T")[0],
                    return_date=result["route"][1]["local_departure"].split("T")[0],
                    out_airline=result["route"][0]["airline"],
                    return_airline=result["route"][1]["airline"],
                    link=result["deep_link"]
                )
                flights.append(flight)
        return flights
