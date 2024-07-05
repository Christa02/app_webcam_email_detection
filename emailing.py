import os
import imghdr
import smtplib
from email.message import EmailMessage

SENDER = "christasaraluke19@gmail.com"
RECEIVER = "christasaraluke19@gmail.com"
PASSWORD = os.getenv("PASSWORD")


def send_email(image_path):
    email_message = EmailMessage()
    email_message['Subject'] = 'New Customer Showed Up!'
    email_message['content'] = 'Hey, A new customer has shown up.'

    with open(image_path, 'rb') as file:
        content = file.read()

    email_message.add_attachment(content,
                                 maintype='image',
                                 subtype=imghdr.what(None, content),
                                 filename='New Customer'
                                 )
    gmail = smtplib.SMTP("smtp.gmail.com", 587, timeout=120)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()
    print('Email Send..................')


if __name__ == "__main__":
    send_email('images/77.png')


