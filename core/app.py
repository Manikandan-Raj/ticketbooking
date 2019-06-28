from rasa_core.channels.slack import SlackInput
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
import yaml
from rasa_core.utils import EndpointConfig
from rasa_nlu.model import Interpreter


model_directory =  Interpreter.load('/Users/vignesh.ramanathan/Desktop/rasa_stack/data/models3/default/model_20190626-162121')

action_endpoint = EndpointConfig(url="http://localhost:5000/webhook")
agent = Agent.load('./models/dialogue_subset', interpreter = model_directory, action_endpoint = action_endpoint)

input_channel = SlackInput('xoxb-662154654626-662172827891-fNu8E28HC7TJEf671ozPnI3N' #your bot user authentication token
                           )

agent.handle_channels([input_channel], 5004, serve_forever=True)
