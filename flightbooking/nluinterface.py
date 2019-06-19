import configparser
import requests
import json

config = configparser.ConfigParser()
config.read("./utils/config.ini")
def extract_entity_from_intent(rs, username, modelname, typed_text):
    nluapi = config["NLU"]["api"]
    print("NLU API---->", nluapi)
    print("MODEL--->", modelname)
    print("Typed Text---->", typed_text)
    url = nluapi + modelname
    data = {}
    data['text'] = typed_text
    headers = {"Content-type":"application/json"}
    print("Calling NLU API------->")
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response = json.loads(response.content)
    print("Response from NLU----->", response)
    print("INtent----->", response['intent']['name'])
    if response['intent']['name'] == "travel" and response['entities']:
        for entity in response['entities']:
            print("Going to set Rive script variables---->")
            rs.set_uservar(username, entity['entity'], entity['value'])
            all_users = rs.get_uservars(rs.current_user())
            print("ALL user variable--->", all_users)
        return "success"
    return "failure"
