from smtplib import SMTPException

from django.core.mail import EmailMessage


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(subject=data['email_subject'], body=data['email_body'], to=[data['email_to']])
        try:
            email.send()
            return 1
        except SMTPException as e:
            print(e)
            return 0