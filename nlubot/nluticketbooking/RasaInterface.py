from rasa_nlu.training_data import load_data
from rasa_nlu.model import Trainer
from rasa_nlu import config
from configparser import SafeConfigParser
from ModelExtracter import ModelExtracter
from CommonVariables import InstanceDict

import os
import json



class RasaInterface(object):
    def __init__(self, model, modelinstance):
        self.model = model
        self.parser = SafeConfigParser()
        self.parser.read('../config/config.ini')
        self.modelextracter = ModelExtracter()

    def train(self, data, update=False):
        # Check if the model is already present and don't want to override
        # delete the existing model
        if self.modelextracter.checkmodel(self.model) and not update:
            self.modelextracter.deletemodel(self.model)
        self.model_folder = self.parser.read("FOLDER", "MODEL")


        if not os.path.exists(self.model_folder + self.model):
            os.mkdir(self.model_folder + self.model)

        nlutrainingdata = self.model_folder+self.model+"/trainingdata.json"
        with open(nlutrainingdata, "w") as f:
            json.dump(data, f, indent=4)

        rasa_config = load_config()
        rasa_config_file = self.model_folder+self.model+"/config.json"
        with open(rasa_config_file, "w") as f:
            json.dump(rasa_config, f, indent=4)

        # Load the data
        training_data = load_data(nlutrainingdata)
        # Prepare the rasa NLU with config for trainer
        trainer = Trainer(config.load(rasa_config_file))

        InstanceDict[self.model] = trainer.train(training_data)
        model_directory = trainer.persist(self.model_folder+self.model)
        if model_directory:
            print("Trainer data is stored in Directory")

    def predict(self, inputtext):
        if InstanceDict[self.model]:
            return InstanceDict.parse(text=inputtext)
        return "No model is present"



    def load_config(self):
        config = {}
        config["language"] = "en"
        config["pipeline"] = "pretrained_embeddings_spacy"
        return config
