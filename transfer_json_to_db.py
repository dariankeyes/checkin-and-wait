from checkin.models import TextMessage

import json


with open('messages.json') as f:
  messages = json.load(f)

  for i in messages:
    message = TextMessage(id=i['id'], message=i['message'], subject=i['subject'])
    message.save()