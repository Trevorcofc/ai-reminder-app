# imports 
from twilio.rest import Client 

# Configs

account_sid = AC88c9898d2839791768c6436078579d23
auth_token = 51bd21338bba151ad291cbcd54d7087d

# Setting up Client 

client = Client(account_sid, auth_token)

# Create the message 

client.messages.create(
  to="5852453824",
  from="6193295136",
  body="This is an automated message sent from Python"
)

from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "AI Reminder App is running!"

if __name__ == '__main__':
    app.run(debug=True)

