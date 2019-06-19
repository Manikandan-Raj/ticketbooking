from rasa_nlu.training_data import load_data
from rasa_nlu.model import Trainer

from rasa_nlu.model import Interpreter
from rasa_nlu import config
from configparser import ConfigParser
from ModelExtracter import ModelExtracter
from flask import jsonify
import os

import json

InstanceLoader = {}

class RasaInterface(object):
    def __init__(self, model):
        self.model = model
        self.parser = ConfigParser()
        self.parser.read('./config/config.ini')
        self.modelextracter = ModelExtracter()

    def train(self, data, update=False):
        # Check if the model is already present and don't want to override
        # delete the existing model
        if self.modelextracter.checkmodel(self.model) and not update:
            self.modelextracter.deletemodel(self.model)
        self.model_folder = self.parser.get("FOLDER", "MODEL")


        if not os.path.exists(self.model_folder + self.model):
            os.mkdir(self.model_folder + self.model)

        nlutrainingdata = self.model_folder+self.model+"/trainingdata.json"
        with open(nlutrainingdata, "w") as f:
            json.dump(data, f, indent=4)

        rasa_config = self.load_config()
        rasa_config_file = self.model_folder+self.model+"/config.json"
        with open(rasa_config_file, "w") as f:
            json.dump(rasa_config, f, indent=4)

        # Load the data
        training_data = load_data(nlutrainingdata)
        # Prepare the rasa NLU with config for trainer
        trainer = Trainer(config.load(rasa_config_file))

        InstanceLoader[self.model] = trainer.train(training_data)

        model_directory = trainer.persist(self.model_folder+self.model)
        if model_directory:
            print("InstanceLoader", InstanceLoader)
            return "Training completed successfully"

    def predict(self, inputtext):
        model_folder = self.parser.get("FOLDER", "MODEL")
        if self.model in InstanceLoader:
            instance = InstanceLoader[self.model]
            response = instance.parse(text=inputtext)
            return jsonify(response)

        else:
            model_folder = self.parser.get("FOLDER", "MODEL")
            if self.model in os.listdir(model_folder):
                model_identification = model_folder + self.model + "/default"
                existing_model = os.listdir(model_identification)[0]
                model_found = model_identification + "/" + existing_model
                instance = Interpreter.load(model_found)
                InstanceLoader[self.model] = instance
                response = instance.parse(text=inputtext)
                return jsonify(response)
            else:
                return "Bot instance is not available"


    def load_config(self):
        config = {}
        config["language"] = "en"
        config["pipeline"] = "pretrained_embeddings_spacy"
        config["projectname"] = self.model
        return config
