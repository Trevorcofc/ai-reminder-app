import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, request 

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html') 

@app.route('/send', methods=['POST'])
def send_message():
    print("FORM DATA:", request.form)
    
    # get user input from the form 
    phone_number = request.form.get('phone number')
    carrier = request.form.get('carrier')
    message_body = request.form.get('message')

    print("Number:", phone_number)
    print("Carrier:", carrier)
    print("Message:", message_body)

    # Create full SMS email address
    to_sms = f"{phone_number}@{carrier}"
    msg['To'] = to_sms
    
    # build the email
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



