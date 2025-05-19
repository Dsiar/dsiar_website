from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
CORS(app)
# Your Gmail credentials
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL") # Fixed destination

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    subject = data.get('subject')
    message = data.get('message')
    phonenumber = data.get('phone')

    if not all([name, email, subject, message, phonenumber]):
        return jsonify({"error": "All fields are required"}), 400

    # Create email
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = f"[Contact Form] {subject} - {name}"

    body = f"""
    You received a new message from the contact form:

    Name: {name}
    Email: {email}
    Subject: {subject}
    PhoneNumber : {phonenumber}
    Message:
    {message}
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Send email via Gmail SMTP
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

        return jsonify({"status":"success", "message": "Your message has been sent successfully."}), 200
    except Exception as e:
        print("line 60", e)
        return jsonify({"status":"error","message": f"Failed to send email: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
