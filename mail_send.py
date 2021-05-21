import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date

today = date.today()
date_formated = today.strftime("%d/%m/%Y")

sender_email = "Knowladge4S@gmail.com"
receiver_email = ["avielro@ac.sce.ac.il", "zivfr@ac.sce.ac.il", "daniera@ac.sce.ac.il", "olegbe@ac.sce.ac.il", "Knowladge4S@gmail.com"]
password = "Know4S!@#"

message = MIMEMultipart("alternative")
message["Subject"] = "Jenkins Test Results " + date_formated
message["From"] = sender_email
message["To"] = ','.join(receiver_email)

def send_result(msg):
    # Turn these into plain/html MIMEText objects
    mail_message = MIMEText(msg, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(mail_message)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )