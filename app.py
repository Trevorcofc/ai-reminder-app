import smtplib
from email.message import EmailMessage
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>✅ AI Reminder App is Running!</h1><p>Next step: create a reminder form.</p>'

@app.route('/send')
def send_message():
    # Define the phone number and carrier gateway
    phone_number = "5859536336"
    carrier_gateway = "vtext.com"  # For Verizon; change based on user’s carrier
    to_sms = f"{phone_number}@{carrier_gateway}"

    # Create the email message
    msg = EmailMessage()
    msg.set_content("Reminder: Hi this is my AI reminder prototype app!")
    msg['Subject'] = "AI Reminder"
    msg['From'] = "ai.reminder.app@gmail.com"
    msg['To'] = to_sms

    # Send the email via Gmail SMTP
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("ai.reminder.app@gmail.com", "ymaocsbfmkpxxgki")  # Use Gmail App Password
            smtp.send_message(msg)
        return "<p>✅ Message sent via email-to-SMS!</p>"
    except Exception as e:
        return f"<p>❌ Failed to send message: {e}</p>"

if __name__ == '__main__':
    app.run(debug=True)



