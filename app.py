from flask import Flask, jsonify
import os
import smtplib
import ssl
from email.message import EmailMessage
from twilio.rest import Client
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Flask app setup
app = Flask(__name__)

def send_sos_alert():
    """ Sends SOS alerts via Email, WhatsApp, Call, and SMS """

    # Email Alert
    def send_email():
        email_sender = os.getenv('EMAIL_SENDER')
        email_password = os.getenv('EMAIL_PASSWORD')
        email_receivers = os.getenv('EMAIL_RECEIVERS').split(',')

        subject = 'SOS ALERT!'
        body = """We have received an SOS alert from you. We are currently reviewing the situation and will get back to you as soon as possible.

        Thank you for your patience.

        Best regards,
        Your Safety Team"""

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
            print("✅ Email successfully sent.")
        except Exception as e:
            print(f"❌ Failed to send email: {str(e)}")

    # WhatsApp Alert
    def send_whatsapp():
        url = 'https://graph.facebook.com/v20.0/380663718469903/messages'
        headers = {
            'Authorization': f'Bearer {os.getenv("WHATSAPP_ACCESS_TOKEN")}',
            'Content-Type': 'application/json'
        }
        phone_numbers = os.getenv('WHATSAPP_NUMBERS').split(',')

        for number in phone_numbers:
            payload = {
                "messaging_product": "whatsapp",
                "to": number,
                "type": "template",
                "template": {
                    "name": "hello_world",
                    "language": {"code": "en_US"}
                }
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                print(f"✅ WhatsApp message sent to {number}")
            else:
                print(f"❌ Failed to send WhatsApp message to {number}: {response.status_code} - {response.text}")

    # Call Alert
    def send_call():
        account_sid = os.getenv('TWILIO_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')

        client = Client(account_sid, auth_token)
        call_numbers = os.getenv('CALL_NUMBERS').split(',')

        for number in call_numbers:
            try:
                call = client.calls.create(
                    url='http://demo.twilio.com/docs/voice.xml',
                    to=number,
                    from_=os.getenv('TWILIO_PHONE_NUMBER')
                )
                print(f"📞 Call initiated to {number}")
            except Exception as e:
                print(f"❌ Failed to initiate call to {number}: {str(e)}")

    # SMS Alert
    def send_sms():
        account_sid = os.getenv('TWILIO_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')

        client = Client(account_sid, auth_token)
        sms_numbers = os.getenv('SMS_NUMBERS').split(',')

        for number in sms_numbers:
            try:
                message = client.messages.create(
                    body="🚨 This is an SOS Alert!",
                    from_=os.getenv('TWILIO_PHONE_NUMBER'),
                    to=number
                )
                print(f"📩 SMS sent to {number}")
            except Exception as e:
                print(f"❌ Failed to send SMS to {number}: {str(e)}")

    # Execute all alerts
    send_email()
    send_whatsapp()
    send_call()
    send_sms()

# Home Route (Fixes 404 Error)
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the SOS Alert API! Use /send_sos to trigger an alert."})

# API Endpoint to Trigger SOS Alerts
@app.route('/send_sos', methods=['POST'])
def api_send_sos():
    try:
        send_sos_alert()
        return jsonify({"status": "success", "message": "🚨 SOS alert sent!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
