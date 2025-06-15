import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, request
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import json
from openai import OpenAI


# Initialize Flask and APScheduler
app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.start()

# 🔑 Set your OpenAI project key here
OPENAI_API_KEY = "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"

client = OpenAI(api_key=OPENAI_API_KEY)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_message():
    phone_number = request.form.get('phone_number')
    carrier = request.form.get('carrier')
    reminder_input = request.form.get('reminder_input')
    to_sms = f"{phone_number}@{carrier}"

    # Extract reminder delay and message using GPT
    parsed = extract_reminder_with_gpt(reminder_input)
    delay_minutes = parsed.get("delay", 0)
    message_body = parsed.get("message", "No message provided")

    # Schedule the reminder
    try:
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
                {"role": "system", "content": "Only respond in JSON format like: {\"delay\": 25, \"message\": \"check the pizza\"}"},
                {"role": "user", "content": f"Remind me: {reminder_input}"}
            ]
        )

        reply_text = response.choices[0].message.content
        print("🧠 GPT Raw Reply:", reply_text)

        # Strip to only JSON if GPT adds extra text
        json_start = reply_text.find("{")
        json_end = reply_text.rfind("}") + 1
        json_text = reply_text[json_start:json_end]

        return json.loads(json_text)

    except Exception as e:
        print("❌ GPT error:", e)
        return {"delay": 0, "message": "Failed to parse reminder"}


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
        print("✅ Sent message to:", to_sms)
    except Exception as e:
        print("❌ Email send error:", e)

if __name__ == '__main__':
    app.run(debug=True)





