import smtplib
from email.mime.text import MIMEText

class Email:

    def send_emails(title, message, recipients):
        for element in recipients:
            Email.send_email(title, message, element)


    def send_email(title, message, recipient):
        sender = 'pomogator2@mail.ru'
        password = '6Y09KjcZKDjgRn63J4AM'
        server = smtplib.SMTP('smtp.mail.ru', 587)
        server.starttls()

        try:
            server.login(sender, password)
            msg = MIMEText(message)
            msg["Subject"] = title
            server.sendmail(sender, recipient, msg.as_string())
            return 'Successful'
        except Exception as _ex:
            return f"{_ex}\nFail"

def main():

    title = input("Your title: ")
    message = input("Your message: ")
    recipients = ['migunovdd@mail.ru', 'migunovdd@gmail.com']
    print(Email.send_emails(title, message, recipients))

if __name__ == '__main__':
    main()