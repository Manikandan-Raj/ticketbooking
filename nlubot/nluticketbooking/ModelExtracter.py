from os import listdir
import shutil
from configparser import ConfigParser


class ModelExtracter(object):
    def __init__(self):
        self.parser = ConfigParser()
        self.parser.read('./config/config.ini')

    def checkmodel(self, instance):
        self.model_folder = self.parser.get("FOLDER", "MODEL")
        print ("Model folder", self.model_folder)
        print ("Type of Model Folder", type(self.model_folder))
        all_models = listdir(self.model_folder)
        if instance in all_models:
            return True
        return False


    def deletemodel(self, instance):
        shutil.rmtree(self.model_folder + instance + "/")
        print("Model is deleted")
