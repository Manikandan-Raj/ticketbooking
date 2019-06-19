import os
import json
from datetime import datetime


def checkavailability(*traveldate, departure, destination):
    print("DATE------>", traveldate)
    print("DEPARTURE------>", departure)
    print("DESTINATION------>", destination)

    available_flight_list = []
    with open("./utils/ticket_backup.json", "r") as outfile:
        flightdb = json.load(outfile)
        for item in flightdb:
            if (item['From'].lower() == departure) and (item['To'].lower() == destination) and checkflightondate(*traveldate, availabledata=item['Date']):
             # (item['Date'].lower() == traveldate[0]):
                flight_details = {}
                flight_details['flightname'] = item['Airlines']
                flight_details['flightno'] = item['Flight No']
                flight_details["availableseats"] = item['Seats']
                flight_details['price'] = item['Price']
                flight_details['date'] = item['Date']
                flight_details['referenceno'] = item["Ref_no"]
                flight_details['connection'] = item["Connection"]

                available_flight_list.append(flight_details)
    print("Matched flight list-->", available_flight_list)
    return available_flight_list


def checkflightondate(*traveldate, availabledata):
    print("Date Comparison in checkflightondate--->",*traveldate)
    print("Type of date--->",traveldate[0])
    if len(traveldate) == 1:
        traveldate = datetime.strptime(traveldate[0], '%d/%m/%Y')
        availabledata = datetime.strptime(availabledata, '%d/%m/%Y')
        return traveldate == availabledata
    else:
        startdate = datetime.strptime(traveldate[0], '%d/%m/%Y')
        enddate = datetime.strptime(traveldate[1], '%d/%m/%Y')
        availabledata = datetime.strptime(availabledata, '%d/%m/%Y')
        return startdate < availabledata < enddate


def checkticket(rs, flightno):
    import json
    flightlist = rs.get_uservar(rs.current_user(), 'availableflightlist')
    flightlist = json.loads(flightlist)
    for item in flightlist[0:-1]:
        if item['flightno'].lower() == str(flightno).lower() and item['availableseats'] > 0:
            return "success"
    return "failure"

def referenceno(rs):
    try:
        import json
        import random
        selectedflight = rs.get_uservar(rs.current_user(), 'selectedflight')
        flightout = []
        referenceno = "failure"
        with open("./utils/ticket_backup.json", "r") as outfile:
            flightdb = json.load(outfile)

            for item in flightdb:
                if item['Flight No'].lower() == selectedflight.lower():
                    reduce_seats = int(item["Seats"]) - 1
                    item["Seats"] = reduce_seats
                    referenceno = random.choice(item["Ref_no"].split(','))
                    flightout.append(item)
                else:
                    flightout.append(item)

        with open("./utils/ticket_backup.json", "w") as file:
            json.dump(flightout, file)
            rs.set_uservar(rs.current_user(), 'referenceno', str(referenceno))
            return "success"
    except Exception as err:
        return str(err)
