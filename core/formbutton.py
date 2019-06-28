def formbutton(actions):
    matched_button_flight = []
    for item in actions:
        flight = {}
        flight["title"] = item["flightname"]
        flight["payload"] = item["flightname"]
        matched_button_flight.append(flight)

    data = {
    "text": "Matched flights for your request",
    "buttons": matched_button_flight,
    "availableflightlist": actions
    }
    return data
