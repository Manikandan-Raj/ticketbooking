## unhappypath_bye_after_departure
* greet
    - utter_greet
* flightbook
    - flightbooking_form
    - form{"name": "flightbooking_form"}
    - slot{"requested_slot": "from"}
* goodbye
    - action_deactivate_form
    - utter_bye
    - action_restart

## unhappypath_bye_after_destination
* greet
    - utter_greet
* flightbook
    - flightbooking_form
    - form{"name": "flightbooking_form"}
    - slot{"requested_slot": "from"}
    - slot{"requested_slot": "to"}
* goodbye
    - action_deactivate_form
    - utter_bye
    - action_restart

## unhappypath_bye_after_date flight
* greet
    - utter_greet
* flightbook
    - flightbooking_form
    - form{"name": "flightbooking_form"}
    - slot{"requested_slot": "from"}
    - slot{"requested_slot": "to"}
    - slot{"requested_slot": "date"}
* goodbye OR greet
    - action_deactivate_form
    - utter_bye
    - action_restart

## unhappypath_bye after_username flight
* greet
    - utter_greet
* flightbook
    - flightbooking_form
    - form{"name": "flightbooking_form"}
* airlinesname
    - action_match
    - flightbookingpersonal_form
    - form{"name": "flightbookingpersonal_form"}
    - slot{"requested_slot": "username"}
* goodbye
    - utter_bye
    - action_deactivate_form
    - action_restart

## unhappypath_bye after_phonenumber flight
* greet
    - utter_greet
* flightbook
    - flightbooking_form
    - form{"name": "flightbooking_form"}
* airlinesname
    - action_match
    - flightbookingpersonal_form
    - form{"name": "flightbookingpersonal_form"}
    - slot{"requested_slot": "username"}
    - slot{"requested_slot": "phonenumber"}
* goodbye
    - utter_bye
    - action_deactivate_form
    - action_restart


## unhappypath_bye after filter the flights
* greet
    - utter_greet
* flightbook
    - flightbooking_form
    - form{"name": "flightbooking_form"}
* flightbook{"mode": "direct"} OR flightbook{"mode": "fastest"} OR flightbook{"mode": "cheapest"}
    - action_filter
* goodbye
    - utter_bye
    - action_deactivate_form
    - action_restart

## happypath with directflight
* greet
    - utter_greet
* flightbook
    - flightbooking_form
    - form{"name": "flightbooking_form"}
* flightbook{"mode": "direct"} OR flightbook{"mode": "fastest"} OR flightbook{"mode": "cheapest"}
    - action_filter
* airlinesname
    - action_match
    - flightbookingpersonal_form
    - form{"name": "flightbookingpersonal_form"}
* goodbye
    - utter_bye
    - action_deactivate_form
    - action_restart

## happypath
* greet
    - utter_greet
* flightbook
    - flightbooking_form
    - form{"name": "flightbooking_form"}
* airlinesname
    - action_match
    - flightbookingpersonal_form
    - form{"name": "flightbookingpersonal_form"}
* goodbye
    - utter_bye
    - action_restart

# Story hi bye
* greet
    - utter_greet
* goodbye
    - utter_bye
    - action_restart

# Story hi bye
* greet
    - utter_greet
* chitchat
    - utter_error_scope_message

## Story chitchat
* chitchat
    - utter_error_scope_message
## Story goodbye
* goodbye
    - utter_bye
    - action_restart


## happypath with directflight
* greet
    - utter_greet
* flightbook
    - flightbooking_form
    - form{"name": "flightbooking_form"}
* flightbook{"mode": "direct"} OR flightbook{"mode": "fastest"} OR flightbook{"mode": "cheapest"}
    - action_filter
* airlinesname
    - action_match
    
