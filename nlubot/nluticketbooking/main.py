from ModelExtracter import ModelExtracter
from flask import Flask, request
from RasaInterface import RasaInterface
import json

APP = Flask(__name__)

modeldetails = ModelExtracter()


@APP.route("/nlu/train/<modelname>", methods=['POST'])
def train(modelname):
    ## TODO: accept the model and check it is present already, then train
    # the model with new data OR else create it
    data = request.data
    print("String format data", data)
    data = json.loads(data)
    print("Requesed data", data)
    trainingdata = data['inputdata']
    rasa_interface = RasaInterface(modelname)
    rasa_interface.train(trainingdata, data.get("update", False))



@APP.route("/nlu/predict/<model>", methods=['POST'])
def predict(model):
    # TODO: Call the model with user text, parse with RaseInterpreter and
    # return the indent and entities
    pass

def format_return_data():
     # TODO: parse the response and re-structure it
     pass


if __name__ == "__main__":
    APP.run()
# training_data = load_data('/home/mani/nlu/py36nlu/data.json')
# trainer = Trainer(config.load("/home/mani/nlu/py36nlu/config_spacy.yml"))
# instance = trainer.train(training_data)
# model_directory = trainer.persist('/home/mani/nlu/py36nlu/nlucode/')
#
# instance.parse(text="good bye")
