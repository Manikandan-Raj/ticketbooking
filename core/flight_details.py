import os
import json
from datetime import datetime
from formbutton import formbutton

def checkavailability(*traveldate, departure, destination):
    import requests
    available_flight_list = []
    print("What are the dates--->", *traveldate)

    with open("/Users/vignesh.ramanathan/Desktop/gitrepoeve/flightbooking/utils/ticket.json", "r") as outfile:
        flightdb = json.load(outfile)
        for item in flightdb:
            if (item['From'].lower() == departure.lower()) and (item['To'].lower() == destination.lower()) and checkflightondate(*traveldate, availabledata=item['Date']):
                flight_details = {}
                flight_details['flightname'] = item['Airlines']
                flight_details['flightno'] = item['Flight No']
                flight_details["availableseats"] = item['Seats']
                flight_details['date'] = item['Date']
                flight_details['referenceno'] = item["Ref_no"]
                flight_details['connection'] = item["Connection"]
                available_flight_list.append(flight_details)


        if available_flight_list:
            print("Matched flight list", available_flight_list)
            return formbutton(available_flight_list)
        else:
            return None




def checkflightondate(*traveldate, availabledata):
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

def referenceno(selectedflight):
    try:
        import json
        import random
        # selectedflight = rs.get_uservar(rs.current_user(), 'selectedflight')
        flightout = []
        referenceno = "failure"
        with open("/Users/vignesh.ramanathan/Desktop/gitrepoeve/flightbooking/utils/ticket.json", "r") as outfile:
            flightdb = json.load(outfile)

            for item in flightdb:
                if item['Airlines'].lower() == selectedflight.lower():
                    reduce_seats = int(item["Seats"]) - 1
                    item["Seats"] = reduce_seats
                    referenceno = random.choice(item["Ref_no"].split(','))
                    flightout.append(item)
                else:
                    flightout.append(item)

        with open("/Users/vignesh.ramanathan/Desktop/gitrepoeve/flightbooking/utils/ticket.json", "w") as file:
            json.dump(flightout, file)
            # rs.set_uservar(rs.current_user(), 'referenceno', str(referenceno))
            print("Going to return ----->", referenceno)
            return referenceno
    except Exception as err:
        return None
