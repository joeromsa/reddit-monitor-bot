import smtplib
import config

class emailbot:

    def __init__(self, subject, msg):
        self.subject = subject
        self.msg = msg

    def send_email(self):
        try:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(config.EMAIL_ADDRESS, config.PASSWORD)
            message = "Subject: {}\n\n{}".format(self.subject, self.msg)
            server.sendmail(config.EMAIL_ADDRESS, config.EMAIL_ADDRESS, message)
            server.quit
            print("Email sent")
        except Exception as err:
            print(err)
