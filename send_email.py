# for mails
import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64


# to_mail If not identified with any authorized person

class emails:

    def sendEmail(self, imgLocation):

        subject = "Un-recognised person is found"
        body = "the underlying person is not recognised by the system. Kindly look over the image."
        sender_email = "raidenrahul1@gmail.com"
        receiver_email = "kumar.rahulsingh01@gmail.com"

        #base64 encoded password looks much more mysterious
        password = base64.b64decode("cGFzc3dvcmQ=").decode("utf-8")

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email

        message.attach(MIMEText(body, "plain"))

        filename = imgLocation

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
