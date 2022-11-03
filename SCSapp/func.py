from datetime import datetime
import pytz
import smtplib
from email.message import EmailMessage

def getUserAuthData(user):
    return {
        'userAuth' : user.is_authenticated,
        "userIsJudge" : user.has_perm('SCS.control_competition'),
    }

def sentMail(message, strRecipients):
    sender = "scsapp@yandex.ru"
    password = 'Prostoparol1234'
    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)

    msg = EmailMessage()
    msg['Subject'] = f'Соревнования скоро!'
    msg['From'] = sender
    msg['To'] = strRecipients
    msg.set_content(message)

    try:
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        return "Messages was sent succesfully"
    except Exception as _e:
        return f"{_e}"