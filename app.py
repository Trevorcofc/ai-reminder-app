import os
import json
import smtplib
import datetime
from email.message import EmailMessage
from flask import Flask, render_template, request
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from openai import OpenAI

# 🔐 Load environment variables from .env file
load_dotenv()

# 🎯 OpenAI client setup
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
print("Loaded OpenAI Key:", os.getenv("OPENAI_API_KEY"))

# 📅 Flask + Scheduler setup
app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.start()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_message():
    phone_number = request.form.get('phone_number')
    carrier = request.form.get('carrier')
    reminder_input = request.form.get('reminder_input')
    to_sms = f"{phone_number}@{carrier}"

    try:
        parsed = extract_reminder_with_gpt(reminder_input)
        delay_minutes = parsed.get("delay", 0)
        message_body = parsed.get("message", "No message provided")

        run_time = datetime.datetime.now() + datetime.timedelta(minutes=delay_minutes)
        scheduler.add_job(
            func=send_email,
            trigger='date',
            run_date=run_time,
            args=[to_sms, message_body]
        )

        return f"<p>✅ AI Reminder scheduled in {delay_minutes} minute(s): {message_body}</p>"

    except Exception as e:
        print("❌ Scheduling error:", e)
        return f"<p>❌ Failed to schedule reminder: {e}</p>"

def extract_reminder_with_gpt(reminder_input):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                  "role": "system",
                  "content": (
                      "You are a reminder parser. Extract the time delay and message from the user's input. "
                      "Always return JSON in the format: {\"delay\": <int>, \"message\": <string>}, where delay is the total number of minutes. "
                      "If the user says '3 hours', convert to 180. If they say '1 hour 30 minutes', return 90. "
                      "Do not include units or any extra explanation — respond only with the raw JSON object."
                   )
                },
                {"role": "user", "content": f"{reminder_input}"}
            ],
            response_format={"type": "json_object"}
        )

        json_data = response.choices[0].message.content
        print("🧠 GPT JSON Reply:", json_data)

        return json.loads(json_data)

    except Exception as e:
        print("❌ GPT error:", e)
        return {"delay": 0, "message": "Failed to parse reminder"}

def send_email(to_sms, message_body):
    msg = EmailMessage()
    msg.set_content(message_body)
    msg['Subject'] = "AI Reminder"
    msg['From'] = os.getenv("GMAIL_ADDRESS")
    msg['To'] = to_sms

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.getenv("GMAIL_ADDRESS"), os.getenv("GMAIL_APP_PASSWORD"))
            smtp.send_message(msg)
        print("✅ Sent message to:", to_sms)
    except Exception as e:
        print("❌ Email send error:", e)

if __name__ == '__main__':
    app.run(debug=True)







