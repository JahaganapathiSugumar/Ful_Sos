from flask import Flask, jsonify, request
import smtplib
import ssl
from email.message import EmailMessage
from twilio.rest import Client
import requests

app = Flask(__name__)

def send_sos_alert():
    # Email Alert
    def send_email():
        email_sender = 'jahaganapathi1@gmail.com'
        email_password = 'bkggefxqikzpbmke'  # Use the app password generated from Google
        email_receivers = [
            'mathavramalingam1608@gmail.com',
            'bavyadharshinir@gmail.com',
            'arunaananthagiri04@gmail.com',
            'deepikagowtham24@gmail.com',
            'sreepriyanth15@gmail.com',
            'jahaganapathi861@gmail.com'
        ]

        subject = 'SOS ALERT!'
        body = """We have received an SOS alert from you. We are currently reviewing the situation and will get back to you as soon as possible.

        Thank you for your patience.

        Best regards,
        Your Company"""

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = ', '.join(email_receivers)
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.starttls(context=context)
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receivers, em.as_string())
            print("Email successfully sent.")
        except Exception as e:
            print(f"Failed to send email. Error: {str(e)}")

    
    # Call Alert
    def send_call():
        account_sid = "AC67e7787e73dea494290e1a54f27ba59a"
        auth_token = "6c2f19b62f3563e4a39b6c07bb6cc932"

        client = Client(account_sid, auth_token)
        call_numbers = [
            {"to": "+916379613654", "name": "JAHA"},
            {"to": "+916382293288", "name": "SREE"}
        ]
        for call_detail in call_numbers:
            call = client.calls.create(
                url='http://demo.twilio.com/docs/voice.xml',
                to=call_detail["to"],
                from_="+17853359244"
            )
            print(f"Call initiated to {call_detail['name']}")

    # SMS Alert
    def send_sms():
        account_sid = "AC67e7787e73dea494290e1a54f27ba59a"
        auth_token = "6c2f19b62f3563e4a39b6c07bb6cc932"

        client = Client(account_sid, auth_token)
        sms_numbers = [
            {"to": "+916382293288", "name": "SREE"},
            {"to": "+916379613654", "name": "JAHA"}
        ]
        for sms_detail in sms_numbers:
            message = client.messages.create(
                body="This is an SOS Alert",
                from_="+17853359244",
                to=sms_detail["to"]
            )
            print(f"SMS sent to {sms_detail['name']}")

    # Execute all alerts
    send_email()
    
    send_call()
    send_sms()


# Flask API setup
@app.route('/', methods=['GET', 'POST'])
def api_send_sos():
    if request.method == 'GET':
        return jsonify({"status": "success", "message": "This endpoint is live!"}), 200

    try:
        send_sos_alert()
        return jsonify({"status": "success", "message": "SOS alert sent!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
