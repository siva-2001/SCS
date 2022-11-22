from datetime import datetime
import pytz
import smtplib
from email.message import EmailMessage

def getUserAuthData(user):
    return {
        'userAuth' : user.is_authenticated,
        "userIsJudge" : user.has_perm('SCS.control_competition'),
    }
