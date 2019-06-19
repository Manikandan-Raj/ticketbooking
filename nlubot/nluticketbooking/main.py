from ModelExtracter import ModelExtracter
from flask import Flask, request, redirect, url_for
from RasaInterface import RasaInterface
import json
from configparser import ConfigParser
from rasa_nlu.model import Metadata, Interpreter

APP = Flask(__name__)
modeldetails = ModelExtracter()

parser = ConfigParser()
parser.read('./config/config.ini')

@APP.route("/nlu/train/<modelname>", methods=['POST'])
def train(modelname):
    """
    Method is used to train the NLU models and persist those model for
    future reference. If you want to override the existing model with new data, pass update as True
    modelname : Name of the directory/model in which trained data will get stored
    sample JSON for training
    {
    "inputdata" : {"rasa_nlu_data": {"common_examples": [<List of JSON>]}
    "update"(optional) : True or False
    }
    """
    data = request.get_json()
    print("Incoming data", data)

    trainingdata = data['inputdata']
    rasa_interface = RasaInterface(modelname)
    rasa_interface.train(trainingdata, data.get("update", False))
    return "Success"

@APP.route("/nlu/predict/<modelname>", methods=['POST'])
def predict(modelname):
    """
    Method used to extract the indent and entities by calling RasaInterface.
    modelname: Name of the model
    sample JSON to predict the results
    {"text":"i want to travel from chennai to Bangalore"}
    """

    data = request.get_json()
    inputtext = data['text']
    rasa_interface = RasaInterface(modelname)
    return rasa_interface.predict(inputtext)


def format_return_data():
     # TODO: parse the response and re-structure it
     pass


if __name__ == "__main__":
    port = int(parser['API']['port'])
    APP.run(port=port)
