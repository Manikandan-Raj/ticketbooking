Interactive chatbot using Rivescript and Python as a Backend

Rive script is used here to maintain the dialogs and conversation
Check here for more details https://www.rivescript.com/

RasaNLU is used to understand the context and extract the entities from indentified intent.
I have added a pre-trained model for Flight Booking.If you want to create new model, please prepare the data by using this
https://rasahq.github.io/rasa-nlu-trainer/ and train the bot.

Macros will act as a middleware layer between our dialogs and backend.
ticket.json file will act as local DB for availability of flights and retrieving the reference number 

Both Chatbot and NLU API's are built using FLASK.
Finally, this chatbot is integrated with Facebook page.

Follow the steps to make this chatbot in your machine

1. Start the NLU, it will load the existing model. If you want to create new nlu model, train it with your data.
2. Start the chatbot API and changing the config file for both chatbot and nlu if needed.
3. Create a APP in facebook check https://developers.facebook.com 
4. Add the webhook url as chatbot API.
5. Createa a page and generate the ACCESS TOKEN and put that in your config file.
6. Select "messages" and "postback" events for the created page.
