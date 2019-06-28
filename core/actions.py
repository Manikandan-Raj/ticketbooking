from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from rasa_core_sdk import Tracker
from rasa_core_sdk.executor import CollectingDispatcher
from rasa_core_sdk.forms import FormAction
from rasa_core_sdk.events import SlotSet


class FlightBookingForm(FormAction):
    """Example of a custom form action"""

    def name(self):
        """Unique identifier of the form"""

        return "flightbooking_form"

    @staticmethod
    def required_slots(tracker: Tracker):
        """A list of required slots that the form has to fill"""
        return ["from", "to", "date"]


    def slot_mappings(self):

          return {
              "from": [
                  self.from_text(not_intent="goodbye")
            ],
              "to": [
                  self.from_text(not_intent="goodbye")
            ],
              "date": [
                  self.from_entity(entity="date", intent="flightbook"),
                  self.from_entity(entity="DATE", intent="flightbook"),
                  self.from_text(not_intent="goodbye")
              ]
          }

    def validate_from(self, value, dispatcher, tracker,domain):
        """Validate from value."""

        latest_message_intent = tracker.latest_message['intent']['name']
        latest_message_entities = tracker.latest_message['entities']
        print("From Intent --------->", latest_message_intent)
        print("From Entities --------->", latest_message_entities)

        intent_list = ["flightbook", "location"]
        entities_list = ["from", "default", "GPE", "ORG"]
        for item in latest_message_entities:
            if item['entity'] in entities_list:
                if latest_message_intent in intent_list:
                    return {"from": item["value"]}
        dispatcher.utter_template("utter_wrong_context", tracker)
        return {"from": None}




    def validate_to(self, value, dispatcher, tracker,domain):
        """Validate to value."""

        latest_message_intent = tracker.latest_message['intent']['name']
        latest_message_entities = tracker.latest_message['entities']
        print("To Intent --------->", latest_message_intent)
        print("To Entities --------->", latest_message_entities)
        intent_list = ["flightbook", "location"]
        entities_list = ["to", "default", "GPE", "ORG"]
        for item in latest_message_entities:
            if item['entity'] in entities_list:
                if latest_message_intent in intent_list:
                    return {"to": item["value"]}

        dispatcher.utter_template("utter_wrong_context", tracker)
        return {"to": None}


    def validate_date(self, value, dispatcher, tracker,domain):
        """Validate from value."""
        print("Date Intent -------->", tracker.latest_message['intent']['name'])
        intent = tracker.latest_message['intent']['name']
        latest_message_entities = tracker.latest_message['entities']
        for item in latest_message_entities:
            print("ENtity--->", item)
            if "date" == item["entity"]:
                tracker.slots['date'] = item["value"]
            elif "enddate" == item["entity"]:
                tracker.slots['enddate'] = item["value"]


        if tracker.get_slot('date') != None:
            return {"date": tracker.get_slot('date')}
        elif tracker.get_slot('enddate') != None:
            return {"date": tracker.get_slot('enddate')}
        else:
            try:
                import datetime
                datetime.datetime.strptime(value, '%d/%m/%Y')
                print("Date---->", value)
                return {"date": value}
            except Exception as err:
                dispatcher.utter_template("utter_wrong_date", tracker)
                # validation failed, set this slot to None, meaning the
                # user will be asked for the slot again
                return {"date": None}


    def submit(self,dispatcher,tracker,domain):
        """Define what the form has to do
            after all required slots are filled"""
        from_place = tracker.get_slot("from")
        to_place = tracker.get_slot("to")
        date = tracker.get_slot("date")
        enddate = tracker.get_slot("enddate")

        import flight_details
        import json
        if enddate != None:
            print("Am calling with start date and enddate--->", date, enddate)
            matched_flight = flight_details.checkavailability(date,enddate, departure=from_place, destination=to_place)
        else:
            print("Am calling with start date--->", date)
            matched_flight = flight_details.checkavailability(date, departure=from_place, destination=to_place)
        if matched_flight:
            dispatcher.utter_button_message(matched_flight["text"], buttons=matched_flight["buttons"])
            return [SlotSet("available_flights", matched_flight["availableflightlist"])]
        else:
            dispatcher.utter_template("utter_no_flights",tracker)
            return []

class FlightBookingPersonalForm(FormAction):
    """Example of a custom form action"""

    def name(self):
        """Unique identifier of the form"""

        return "flightbookingpersonal_form"

    @staticmethod
    def required_slots(tracker: Tracker):
        """A list of required slots that the form has to fill"""
        if tracker.get_slot('selectedflight'):
            return ["username", "phonenumber", "aadhaar"]
        return []

    def slot_mappings(self):
        return {
            "username": [
                self.from_entity(entity="username",intent="personalinfo"),
                self.from_text(not_intent="goodbye")
            ],
            "phonenumber": [
                self.from_entity(entity="phonenumber",intent="personalinfo"),
                self.from_entity(entity="CARDINAL",intent="personalinfo"),
                self.from_text(not_intent="goodbye")
            ],
            "aadhaar": [
                self.from_entity(entity="aadhaar",intent="personalinfo"),
                self.from_entity(entity="CARDINAL",intent="personalinfo"),
                self.from_text(not_intent="goodbye")
            ],
        }
    def validate_username(self, value, dispatcher, tracker,domain):
        """Validate name value."""
        import personalinformation
        match = personalinformation.personalinfoname(value)
        print("MATCHING VALUE value for username------>", match)
        if match:
            # validation succeeded, set the value of the "username" slot to value
            print("SLOT value for username------>", value)
            return {"username": value}
        else:
            dispatcher.utter_template("utter_wrong_username", tracker)
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"username": None}

    def validate_phonenumber(self, value, dispatcher, tracker,domain):
        """Validate phonenumber value."""
        import personalinformation
        if personalinformation.personalinfophone(value):
            # validation succeeded, set the value of the "phonenumber" slot to value
            print("SLOT value for phonenumber------>", value)
            return {"phonenumber": value}
        else:
            dispatcher.utter_template("utter_wrong_phonenumber", tracker)
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"phonenumber": None}

    def validate_aadhaar(self, value, dispatcher, tracker,domain):
        """Validate aadhaar value."""
        import personalinformation
        if personalinformation.personalinfoid(value):
            # validation succeeded, set the value of the "aadhaar" slot to value
            print("SLOT value for aadhaar------>", value)
            return {"aadhaar": value}
        else:
            dispatcher.utter_template("utter_wrong_aadhaar", tracker)
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"aadhaar": None}


    def submit(self,dispatcher,tracker,domain):
        """Define what the form has to do
            after all required slots are filled"""
        selectedflight = tracker.get_slot("selectedflight")
        print("What is selected flight", selectedflight, "and type", type(selectedflight))
        import flight_details
        import json
        matched_flight = flight_details.referenceno(selectedflight)
        if matched_flight:
            dispatcher.utter_template("utter_ticket_book",tracker, referenceno= matched_flight)
            return []
        else:
            dispatcher.utter_template("utter_no_ticket",tracker)
            return []



from rasa_core_sdk import Action

class ActionGetSelectedFlight(Action):

    def name(self):
        return "action_match"

    def run(self,dispatcher,tracker,domain):
        latest_message_intent = tracker.latest_message['intent']['name']
        entitieslist = tracker.latest_message['entities']
        if len(entitieslist) > 0:
            entity_name = entitieslist[0]["value"]

            dispatcher.utter_template('utter_ask_selected_flight',tracker, name=entity_name)
            return [SlotSet("selectedflight", entity_name)]
        else:
            dispatcher.utter_template('utter_error_scope_message', tracker)
            return []

from rasa_core_sdk import Action

class ActionCheckFrom(Action):

    def name(self):
        return "action_filter"

    def run(self,dispatcher,tracker,domain):
        import formbutton
        filtered_list = []
        mode = tracker.get_slot("mode")

        if mode.lower() == "direct" or mode.lower() == "fastest":
            connection = True
        else:
            connection = False
        flight_list = tracker.get_slot("available_flights")


        if connection:
            filtered_list = [item for item in flight_list if item["connection"] == "True"]
        else:
            filtered_list = [item for item in flight_list if item["connection"] == "False"]
        print("filter list--->", filtered_list)
        if filtered_list != None:
            filter = formbutton.formbutton(filtered_list)

            dispatcher.utter_button_message(filter["text"], buttons=filter["buttons"])
            return []
        else:
            dispatcher.utter_message("No % flight from this places"%mode)
            return []
