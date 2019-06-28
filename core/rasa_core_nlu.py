from rasa_nlu.model import Interpreter
import asyncio
from rasa_core.agent import Agent
import rasa_core
model_directory =  Interpreter.load('/Users/vignesh.ramanathan/Desktop/rasa_stack/formaction/models/sample/nlu')
agent=Agent.load('/Users/vignesh.ramanathan/Desktop/rasa_stack/formaction/models/sample/core', interpreter=model_directory, action_endpoint = "http://localhost:5055/webhook")


# rasa_core.run.serve_application(agent ,channel='cmdline')
agent.handle_channel(ConsoleInputChannel())
# while True:
#     msg = input('User>')
#     if msg == 'quit':
#         quit()
#
#     responses =  agent.handle_channel(ConsoleInputChannel())
#     print("MSG", responses['text'])
#     print("Type of handle_message", type(responses))
#     for response in responses:
#         print("Bot>", response['text'])
#         print("Options>", response.get("buttons"))
