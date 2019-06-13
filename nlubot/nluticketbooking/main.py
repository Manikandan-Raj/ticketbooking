from ModelExtracter import ModelExtracter
from flask import Flask, request
from RasaInterface import RasaInterface
import json

from rasa_nlu.model import Metadata, Interpreter


APP = Flask(__name__)

modeldetails = ModelExtracter()


@APP.route("/nlu/train/<modelname>", methods=['POST'])
def train(modelname):
    ## TODO: accept the model and check it is present already, then train
    # the model with new data OR else create it
    data = request.get_json()
    print("Incoming data", data)
    print("Type of incoming data", type(data))
    trainingdata = data['inputdata']
    rasa_interface = RasaInterface(modelname)
    return rasa_interface.train(trainingdata, data.get("update", False))



@APP.route("/nlu/predict/<modelname>", methods=['POST'])
def predict(modelname):
    # TODO: Call the model with user text, parse with RaseInterpreter and
    # return the indent and entities

    data = request.get_json()
    inputtext = data['text']
    rasa_interface = RasaInterface(modelname)
    return rasa_interface.predict(inputtext)



def format_return_data():
     # TODO: parse the response and re-structure it
     pass


if __name__ == "__main__":
    APP.run()
