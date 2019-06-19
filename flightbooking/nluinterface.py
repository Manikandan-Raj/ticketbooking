import configparser
import requests
import json

config = configparser.ConfigParser()
config.read("./utils/config.ini")
def extract_entity_from_intent(rs, username, modelname, typed_text):
    nluport = config["NLU"]["port"]
    nluapi = "http://localhost:"+nluport+"/nlu/predict/"
    url = nluapi + modelname
    data = {}
    data['text'] = typed_text
    headers = {"Content-type":"application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response = json.loads(response.content)
    if response['intent']['name'] == "travel" and response['entities']:
        for entity in response['entities']:
            rs.set_uservar(username, entity['entity'], entity['value'])
        return "success"
    return "failure"
