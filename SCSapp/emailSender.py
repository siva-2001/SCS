import smtplib
import os
from email import encoders
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

class Email:
    SENDER_ADRES = 'pomogator2@mail.ru'
    PASSWORD = '6Y09KjcZKDjgRn63J4AM'
    SERVER_ADRES = 'smtp.mail.ru'
    PORT = 587

    def send_emails(self, title, message, recipients, file):
        try:
            for element in recipients: self.send_email(title, message, element, file)
            return 'Successful'
        except Exception as _ex: return f"{_ex}"

    def send_email(self, title, message, recipient, filePathes):

        server = smtplib.SMTP(self.SERVER_ADRES, self.PORT)
        server.starttls()
        server.ehlo()

        server.login(self.SENDER_ADRES, self.PASSWORD)
        msg = MIMEMultipart()
        msg["Subject"] = title
        msg.attach(MIMEText(message))

        for file in filePathes:

            filename = os.path.basename(file)
            ftype, encoding = mimetypes.guess_type(file)
            file_type, subtype = ftype.split("/")

            with open(file, "rb") as f:
                file = MIMEBase(file_type, subtype)
                file.set_payload(f.read())
                encoders.encode_base64(file)

            file.add_header('content-disposition', 'attachment', filename=filename)
            msg.attach(file)
        print(server.sendmail(self.SENDER_ADRES, recipient, msg.as_string()))

def main():
    title = "SCS. Тестирование рассылки мейлов"
    message = "some text"
    recipients = [
        'pomogator2@mail.ru',
        'slava.kutolvas@gmail.com',
        'migunovdd@gmail.com',
        'igran2001@gmail.com',
        'georgii2911@gmail.com',
    ]
    filePath = "D:/chechen.png"
    filePathes = [
        "D:/chechen.png",
        "D:/gun.png"
    ]
    sender = Email()
    print(sender.send_emails(title, message, recipients, filePathes))

if __name__ == '__main__':
    main()