from flask import Flask

app = Flask(__name__)

@app.route("/nlu/train/<model>", methods=['POST'])
def train(model):
    ## TODO: accept the model and check it is present already, then train
    # the model with new data OR else create it
    pass


@app.route("/nlu/predict/<model>", methods=['POST'])
def predict(model):
    # TODO: Call the model with user text, parse with RaseInterpreter and
    # return the indent and entities
    pass

 def format_return_data():
     # TODO: parse the response and re-structure it
     pass


from rasa_nlu.training_data import load_data
from rasa_nlu.model import Trainer
from rasa_nlu import config
training_data = load_data('/home/mani/nlu/py36nlu/data.json')
trainer = Trainer(config.load("/home/mani/nlu/py36nlu/config_spacy.yml"))
instance = trainer.train(training_data)
model_directory = trainer.persist('/home/mani/nlu/py36nlu/nlucode/')

instance.parse(text="good bye")
