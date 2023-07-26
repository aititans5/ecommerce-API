import smtplib, ssl
import os

port = 465  # For SSL
password = os.environ.get('EMAIL_PASSWORD')
sender_email = "aititans5group@gmail.com"
# Create a secure SSL context
context = ssl.create_default_context()

'''Send plain text email'''
def sendPlainTextEmail(receiver_email, message):
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)



