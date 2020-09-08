from ..models import Checkin, TextMessage, Word
from .sms import send_sms

from django.shortcuts import get_object_or_404


# receives sms and determines response
def process_received_sms(from_number, received_sms):
    received_sms = received_sms.lower().strip()
    # check_in_words = ['here']
    # opt_in_words = ['start', 'subscribe', 'unstop', 'enroll']
    # opt_out_words = ['end', 'quit', 'stop', 'stopall', 'unsubscribe']
    # help_words = ['help', 'info']
    # cancel_words = ['cancel', 'cancel checkin', 'cancel check-in']

    check_in_words = Word.objects.word_list(category='check_in_words')
    opt_in_words = Word.objects.word_list(category='opt_in_words')
    opt_out_words = Word.objects.word_list(category='opt_out_words')
    help_words = Word.objects.word_list(category='help_words')
    cancel_words = Word.objects.word_list(category='cancel_words')

    # re-write this to prevent duplicate check-in
    if received_sms in check_in_words[0]:
        # verifies that the associate doesn't have an open checkin
        if Checkin.objects.filter(phone_number=from_number, canceled=None, notification_text=None).exists():
            message = "You're already checked in. " \
                      "Please wait and we'll notify you as soon as you can come into the building."
            send_sms(from_number, message)
        # if not, checks associate in
        else:
            count = Checkin.waiting.all().count() + 1
            check_in = Checkin(phone_number=from_number)
            check_in.save()
            # message = "You've been checked in! " \
            #           "You'll receive a second text once we can see you. " \
            #           "You are currently #" + str(count) + " in line."
            message = TextMessage.objects.get_text(subject='first contact')
            send_sms(from_number, message)

    # Cancel Request
    elif received_sms in cancel_words:
        if Checkin.objects.filter(phone_number=from_number, canceled=None, notification_text=None).exists():
            check_in = Checkin.objects.get(phone_number=from_number, canceled=None, notification_text=None)
            check_in.canceled = True
            check_in.save()
            message = "Your checkin has been cancelled."
            send_sms(from_number, message)
        else:
            message = "You have no open check-in. Please text Here if you are needing to check-in."
            send_sms(from_number, message)

    # if user sends Opt-In, Opt-Out, or Help text, don't send any response.
    # Twilio sends a response that is defined in the Twilio console
    elif received_sms in opt_in_words or received_sms in opt_out_words or received_sms in help_words:
        pass

    # Anything else would be considered an invalid response
    else:
        message = TextMessage.objects.get_text(subject='invalid response')
        send_sms(from_number, message)

