import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, request
from apscheduler.schedulers.background import BackgroundScheduler
import datetime

app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.start()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_message():
    # Get user input from the form
    phone_number = request.form.get('phone_number')
    carrier = request.form.get('carrier')
    message_body = request.form.get('message')
    delay_minutes = int(request.form.get('delay', 0))  # Default to 0 if not provided

    # Construct SMS email
    to_sms = f"{phone_number}@{carrier}"

    # Calculate send time
    run_time = datetime.datetime.now() + datetime.timedelta(minutes=delay_minutes)

    # Schedule the email to be sent later
    scheduler.add_job(
        func=send_email,
        trigger='date',
        run_date=run_time,
        args=[to_sms, message_body]
    )

    return f"<p>⏰ Reminder scheduled in {delay_minutes} minute(s)!</p>"

# Function to send the email
def send_email(to_sms, message_body):
    msg = EmailMessage()
    msg.set_content(message_body)
    msg['Subject'] = "AI Reminder"
    msg['From'] = "ai.reminder.app@gmail.com"
    msg['To'] = to_sms

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("ai.reminder.app@gmail.com", "ymaocsbfmkpxxgki")
            smtp.send_message(msg)
        print("✅ Sent scheduled message to:", to_sms)
    except Exception as e:
        print("❌ Failed to send scheduled message:", e)

if __name__ == '__main__':
    app.run(debug=True)



