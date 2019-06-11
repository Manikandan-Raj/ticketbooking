from rivescript import RiveScript
from flask import Flask

BOT = RiveScript()
BOT.load_directory("C:\\rstut\\rivescript\\")
BOT.sort_replies()
APP = Flask(__name__)

while True:
    msg = raw_input('You> ')
    if msg == '/quit':
        quit()

    reply = BOT.reply("localuser", msg)
    print 'Bot>', reply
