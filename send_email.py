# for mails
import smtplib, ssl
from send_email import encoders
from send_email.mime.base import MIMEBase
from send_email.mime.multipart import MIMEMultipart
from send_email.mime.text import MIMEText


# to_mail If not identified with any authorized person
# pass image into function
# can include data entry to a csv file


class email:
    def sendEmail(self):
        subject = "An email with attachment from Python"
        body = "This is an email with attachment sent from Python"
        sender_email = "raidenrahul1@gmail.com"
        receiver_email = "kumar.rahulsingh01@gmail.com"
        password = "Self2Learnd&"

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email

        message.attach(MIMEText(body, "plain"))

        filename = "flaskImage.jpg"

        # Open image file in binary mode
        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)

        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        message.attach(part)
        text = message.as_string()

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)
