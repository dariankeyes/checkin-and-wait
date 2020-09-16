from django.conf import settings
from ..models import TwilioMessages

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

import json


def send_sms(phone_number, sms_to_send):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    status_callback = settings.TWILIO_CALLBACK_URL
    client = Client(account_sid, auth_token)
    try:
        message = client.messages.create(
            to=phone_number,
            from_=settings.TWILIO_NUMBER,
            body=sms_to_send,
            status_callback=status_callback
        )

        # creates database record of outgoing message
        twilio_message = TwilioMessages(sent_message_sid=message.sid, body=message.body,
                                        phone_number=message.to, status=message.status,
                                        type='outgoing_message')
        twilio_message.save()

        if message.status:
            success = True
            message = "SMS sent to " + phone_number
            data = {'message': message, 'success': success}
            return data
        else:
            success = False
            message = "Unknown Error! failed to send. Retry"
            data = {'message': message, 'success': success}
            return data

    except TwilioRestException as e:
        print(e)
        if e.code == 21211:
            success = False
            message = "Invalid Phone Number. Try Again! " + str(phone_number)
            data = {'message': message, 'success': success}
            return data
        elif e.code == 21610:
            success = False
            message = "Looks like you've opted out. To re-enroll, text START to" \
                      "" + str(settings.TWILIO_NUMBER) + ". Then try again."
            data = {'message': message, 'success': success}
            return data
        else:
            success = False
            message = "Invalid Phone Number. Try Again! " + str(phone_number)
            data = {'message': message, 'success': success}
            return data


def get_sms_history():
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    messages = client.messages.list()

    print(len(messages))
    # for record in messages:
    #     print(record.body)

# https://api.twilio.com/2010-04-01/Accounts/AC72b6962bbe9a8a7a4f1bf13a9249cd0b/Messages.csv?PageSize=1000
