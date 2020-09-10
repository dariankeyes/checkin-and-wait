from ..models import Checkin, TextMessage
from .sms import send_sms

from django.conf import settings


# receives sms and determines response
def process_received_sms(from_number, received_sms):
    received_sms = received_sms.lower().strip()

    check_in_words = settings.CHECK_IN_WORDS
    opt_in_words = settings.OPT_IN_WORDS
    opt_out_words = settings.OPT_OUT_WORDS
    help_words = settings.HELP_WORDS
    cancel_words = settings.CANCEL_WORDS

    # checks customer in
    if received_sms in check_in_words[0]:
        # verifies that the associate doesn't have an open checkin
        if Checkin.objects.filter(phone_number=from_number, canceled=None, notification_text=None).exists():
            message = TextMessage.objects.get_text(subject='already_checked_in_response')
            send_sms(from_number, message)
        # if not, checks associate in
        else:
            count = Checkin.waiting.all().count() + 1
            check_in = Checkin(phone_number=from_number)
            check_in.save()
            message = TextMessage.objects.get_text(subject='first contact')
            send_sms(from_number, message)

    # Cancel Request
    elif received_sms in cancel_words:
        if Checkin.objects.filter(phone_number=from_number, canceled=None, notification_text=None).exists():
            check_in = Checkin.objects.get(phone_number=from_number, canceled=None, notification_text=None)
            check_in.canceled = True
            check_in.save()
            message = TextMessage.objects.get_text(subject='cancellation_response')
            send_sms(from_number, message)
        else:
            message = TextMessage.objects.get_text(subject='invalid_cancellation_request')
            send_sms(from_number, message)

    # if user sends Opt-In, Opt-Out, or Help text, don't send any response.
    # Twilio sends a response that is defined in the Twilio console
    elif received_sms in opt_in_words or received_sms in opt_out_words or received_sms in help_words:
        pass

    # Anything else would be considered an invalid response
    else:
        message = TextMessage.objects.get_text(subject='invalid response')
        send_sms(from_number, message)

