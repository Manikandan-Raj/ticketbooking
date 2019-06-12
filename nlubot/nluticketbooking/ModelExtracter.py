from os import listdir
import shutil
from configparser import SafeConfigParser


class ModelExtracter(object):
    def __init__(self):
        self.parser = SafeConfigParser()
        self.parser.read('../config/config.ini')

    def checkmodel(self, instance):
        self.model_folder = self.parser.read("FOLDER", "MODEL")
        all_models = listdir(model_folder)
        if instance in all_models:
            return True
        return False


    def deletemodel(self, instance):
        shutil.rmtree(self.model_folder + instance + "/")
        print("Model is deleted")
