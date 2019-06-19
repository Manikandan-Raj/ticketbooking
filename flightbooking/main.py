from rivescript import RiveScript
from flask import Flask, request, session
import json
import requests
import threading
from configparser import ConfigParser
parser = ConfigParser()
parser.read('./utils/config.ini')

BOT = RiveScript(utf8=True)
BOT.load_directory("../rivescript")
BOT.sort_replies()
APP = Flask(__name__)
APP.secret_key = "Rivescript-chatbot"

PAGE_ACCESS_TOKEN = parser['FACEBOOK']['page_access_token']

FACEBOOK_RESPONSE_URL = parser['FACEBOOK']['url']

@APP.route("/", methods=["GET", "POST"])
def get_details():
    """
    Mehod is used to getting a reply from Rivescript
    """
    if request.method == 'GET':
      token = request.args.get('hub.verify_token')
      challenge = request.args.get('hub.challenge')
      if token == "secret":
          return str(challenge)
      return '200'

    elif request.method == 'POST':
        data = request.data
        thread = threading.Thread(target=callbackmethod,  args=(data,))
        thread.start()

        return '200'

def callbackmethod(data):
    data = json.loads(data)
    messaging = data.get('entry')[0].get('messaging')[0]
    sender_id = messaging.get('sender').get('id')
    if messaging.get('message', None):
        user_typed_msg = messaging['message'].get('text')
    elif messaging.get('postback'):
        user_typed_msg = messaging['postback'].get('payload')

    headers = {"Content-Type":"application/json"}
    url = FACEBOOK_RESPONSE_URL + PAGE_ACCESS_TOKEN

    BOT.set_uservar(sender_id,"typed_text",user_typed_msg)
    bot_reply = BOT.reply(sender_id, user_typed_msg, errors_as_replies=False)
    print("Message from Bot------>", bot_reply)
    if bot_reply.find("=>") != -1:
        index = bot_reply.index("=>") + 3
        bot_reply = bot_reply[index:]
    bot_reply = json.loads(bot_reply)
    options = bot_reply['options']
    post_data = None
    if options:
        if "quick_replies" in options:
            bot_reply['options'] = bot_reply['options'][0:-1]
            post_data = form_quick_replies(bot_reply, sender_id)
        elif "list_replies" in options:
            bot_reply['options'] = bot_reply['options'][0:-1]
            post_data = form_list_template(bot_reply, sender_id)
    else:
        post_data = normal_reply(bot_reply,sender_id)

    res = requests.post(url=url, headers=headers, data=json.dumps(post_data))


def form_quick_replies(data, sender_id):
    sender_details = {"id": sender_id}

    form_replies = []
    for item in data["options"]:
        reply = {}
        reply["content_type"] = "text"
        reply["title"] = item
        reply["payload"] = item
        form_replies.append(reply)

    reply_to_user= {
            "text": data['text'],
            "quick_replies": form_replies
    }

    post_data = {}
    post_data["messaging_type"] = "RESPONSE"
    post_data["recipient"] = sender_details
    post_data["message"] = reply_to_user
    return post_data

def form_list_template(data,sender_id):
    sender_details = {"id": sender_id}

    buttonlist =[]
    for item in data['options']:
        template = {}
        template["type"] = "postback"
        template["title"] = item["flightname"]+"\n"+item["flightno"]
        template["payload"] = item["flightno"]
        buttonlist.append(template)

    reply_to_user = {
        "attachment":{
          "type":"template",
          "payload":{
            "template_type":"button",
            "text": data['text'],
            "buttons": buttonlist
            }
        }
    }

    post_data = {}
    post_data["recipient"] = sender_details
    post_data["message"] = reply_to_user
    return post_data

def normal_reply(data,sender_id):
    sender_details = {"id": sender_id}
    post_data = {}
    post_data["messaging_type"] = "RESPONSE"
    post_data["recipient"] = sender_details
    post_data["message"] = {"text":data['text']}
    return post_data


if __name__ == "__main__":
    port = int(parser['CHATBOT']['port'])
    APP.run(port=port)
