import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, request
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import openai
import json  # use this instead of eval()

# Set your OpenAI API key (secure version recommended)
client = openai.OpenAI(api_key="your-openai-key-here")

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

    prompt = f"""Extract the reminder delay (in minutes) and message from this request:
    "{reminder_input}"
    Respond in JSON like this: {{ "delay": 25, "message": "check the pizza" }}"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Extract the delay (in minutes) and reminder message from the user's request."},
                {"role": "user", "content": prompt}
            ]
        )
        gpt_reply = response.choices[0].message.content
        parsed = json.loads(gpt_reply)  # safer than eval()

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
        print("❌ GPT or schedule error:", e)
        return f"<p>❌ Failed to process reminder: {e}</p>"

def send_email(to_sms, message_body):
    msg = EmailMessage()
    msg.set_content(message_body)
    msg['Subject'] = "AI Reminder"
    msg['From'] = "ai.reminder.app@gmail.com"
    msg['To'] = to_sms

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("ai.reminder.app@gmail.com", "your-app-password-here")
            smtp.send_message(msg)
        print("✅ Sent message to:", to_sms)
    except Exception as e:
        print("❌ Email send error:", e)

if __name__ == '__main__':
    app.run(debug=True)



