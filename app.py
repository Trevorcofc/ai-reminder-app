from flask import Flask
from twilio.rest import Client

# Flask setup
app = Flask(__name__)

@app.route('/')
def home():
    print("🏠 Home page accessed")
    return '<h1>✅ AI Reminder App is Running!</h1><p>Next step: create a reminder form.</p>'


@app.route('/send')
def send_message():
    # Twilio Configs
    account_sid = "AC88c9898d2837971768c6430678579d23"
    auth_token = "51bd21338bba151ad291cbc5d54708d7"
    client = Client(account_sid, auth_token)

    # Send the message
    message = client.messages.create(
        to="+15852453824",     # Add +1 if it's a US number
        from="+16192952136",  # Use the Twilio number in E.164 format
        body="This is an automated message sent from Python!"
    )

    return f'<p>✅ Message sent! SID: {message.sid}</p>'

if __name__ == '__main__':
    app.run(debug=True)


