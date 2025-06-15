import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_message():
    # Get user input from the form
    phone_number = request.form.get('phone_number')  
    carrier = request.form.get('carrier')
    message_body = request.form.get('message')

    to_sms = f"{phone_number}@{carrier}"

    try:
        msg = EmailMessage()
        msg.set_content(message_body)
        msg['Subject'] = "AI Reminder"
        msg['From'] = "ai.reminder.app@gmail.com"
        msg['To'] = to_sms

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("ai.reminder.app@gmail.com", "ymaocsbfmkpxxgki")  # Use App Password
            smtp.send_message(msg)

        return "<p>✅ Message sent via email-to-SMS!</p>"

    except Exception as e:
        return f"<p>❌ Failed to send message: {e}</p>"

if __name__ == '__main__':
    app.run(debug=True)




