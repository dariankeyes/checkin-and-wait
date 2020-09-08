from django.conf import settings
from ..models import Checkin, TextMessage

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


def west_send_sms(phone_number, sms_to_send):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    try:
        message = client.messages.create(
            to=phone_number,
            from_=settings.TWILIO_NUMBER,
            body=sms_to_send
        )
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
            message = "Check in failed! You'll need to text START to " \
                      "" + str(settings.TWILIO_NUMBER) + ". Then try again."
            data = {'message': message, 'success': success}
            return data
        else:
            success = False
            message = "Invalid Phone Number. Try Again! " + str(phone_number)
            data = {'message': message, 'success': success}
            return data





# Instantiate the API client and create a controller for Messages
client = FlowroutenumbersandmessagingClient(basic_auth_user_name, basic_auth_password)
messages_controller = client.messages

# Create your test SMS
request_body = '{ \
      "data": { \
        "type": "message", \
        "attributes": { \
          "to": "+YOUR_MOBILE_NUMBER", \
          "from": "+YOUR_FLOWROUTE_NUMBER", \
          "body": "hey" \
        } \
      } \
    }'

print ("---Send A Message")
result = messages_controller.send_a_message(request_body)
pprint.pprint(result)
