import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, request
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import openai
import os

openai.api_key = "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"

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

    # 🔍 Use GPT to extract delay + message
    prompt = f"""Extract the reminder delay (in minutes) and message from this request:
    "{reminder_input}"
    Respond in JSON like this: {{"delay": 25, "message": "check the pizza"}}"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        gpt_reply = response['choices'][0]['message']['content']
        parsed = eval(gpt_reply)  # Safe here only if you're controlling input
        delay_minutes = parsed.get("delay", 0)
        message_body = parsed.get("message", "No message provided")

        # Schedule with APScheduler
        run_time = datetime.datetime.now() + datetime.timedelta(minutes=delay_minutes)
        scheduler.add_job(
            func=send_email,
            trigger='date',
            run_date=run_time,
            args=[to_sms, message_body]
        )

        return f"<p>✅ AI Reminder scheduled in {delay_minutes} minute(s): {message_body}</p>"

    except Exception as e:
        print("❌ GPT or schedule error:", e)
        return f"<p>❌ Failed to process reminder: {e}</p>"


if __name__ == '__main__':
    app.run(debug=True)



