import smtplib
import os
from email import encoders
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

class Email:

    def send_emails(title, message, recipients, file):
        try:
            for element in recipients:
                Email.send_email(title, message, element, file)
            return 'Successful'
        except Exception as _ex:
            return f"{_ex}\nFail"

    def send_email(title, message, recipient, file):
        sender = 'pomogator2@mail.ru'
        password = '6Y09KjcZKDjgRn63J4AM'
        server = smtplib.SMTP('smtp.mail.ru', 587)
        server.starttls()

        try:
            server.login(sender, password)
            msg = MIMEMultipart()
            msg["Subject"] = title
            msg.attach(MIMEText(message))

            filename = os.path.basename(file)
            ftype, encoding = mimetypes.guess_type(file)
            file_type, subtype= ftype.split("/")

            with open(file, "rb") as f:
                file = MIMEBase(file_type, subtype)
                file.set_payload(f.read())
                encoders.encode_base64(file)

            file.add_header('content-disposition', 'attachment', filename = filename)
            msg.attach(file)

            server.sendmail(sender, recipient, msg.as_string())
            return 'Successful'
        except Exception as _ex:
            return f"{_ex}\nFail"

def main():

    title = input("Your title: ")
    message = input("Your message: ")
    recipient = 'migunovdd@mail.ru'
    recipients = ['migunovdd@mail.ru', 'migunovdd@gmail.com']
    print(Email.send_emails(title, message, recipients, "D:/chechen.png"))

if __name__ == '__main__':
    main()