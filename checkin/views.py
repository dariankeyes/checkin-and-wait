from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from django.utils import timezone


from .forms import CheckinForm
from .models import Checkin, TextMessage, TwilioMessages
from .supporting_scripts.sms import send_sms
from .supporting_scripts.process_received_sms import process_received_sms

import logging

logger = logging.getLogger(__name__)

app_name = settings.CHECKIN_APP_NAME


# Create your views here.
def home(request):
    title = 'Otis Corley'
    template = 'home.html'

    if request.method == "POST":
        form = CheckinForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone_number']
            sms_to_send = TextMessage.objects.get_text(subject='first contact')
            response = send_sms(phone, sms_to_send)
            if response['success']:
                form.save()
                message = "Check In successful. You should receive a text from us shortly."
                return redirect('checkin_confirmation', message)
            else:
                message = response['message']
                return redirect('checkin_confirmation', message)
    else:
        form = CheckinForm()
        # checks if check in page should show a message
        if TextMessage.objects.filter(subject='check in page').exists():
            message = TextMessage.objects.get_text(subject='check in page')
            context = {'app_name': app_name, 'title': title, 'form': form, 'message': message}
        else:
            context = {'app_name': app_name, 'title': title, 'form': form}
        return render(request, template, context)


def checkin_confirmation(request, message):
    title = "All Set!"
    template = "checkin_confirmation.html"
    return render(request, template, {'title': title, 'message': message})


@login_required
def dashboard(request):
    title = 'Currently Waiting'
    template = 'dashboard/dashboard.html'
    waiting = Checkin.objects.all()
    return render(request, template, {'app_name': app_name, 'title': title, 'waiting': waiting})


def terms(request):
    title = 'Terms of Use'
    template = 'terms.html'
    return render(request, template, {'app_name': app_name, 'title': title})


@login_required
def message_config(request):
    template = 'dashboard/settings.html'

    messages = TextMessage.objects.all()

    return render(request, template, {'app_name': app_name, 'messages': messages})


@csrf_exempt
def get_check_ins(request):
    check_ins = list(Checkin.waiting.all())
    return JsonResponse(check_ins, safe=False)


@csrf_exempt
def send_ready_notification(request):
    pk = request.GET['pk']
    check_in = get_object_or_404(Checkin, pk=pk)
    message = {'body': '', 'subject': ''}

    # if check_in has been marked as cancelled
    if check_in.canceled:
        message['body'] = "Customer Cancelled Checkin"
        message['subject'] = "Customer initiated a cancellation"
    # if someone else has already sent a notification text
    elif check_in.notification_text:
        message['body'] = "Notification already sent to " + check_in.phone_number
        message['subject'] = "Notification Status"
    # send sms runs
    else:
        sms_to_send = TextMessage.objects.get_text(subject='ready notification')
        response = send_sms(check_in.phone_number, sms_to_send)
        # Notification text successfully sent
        if response['success']:
            message['body'] = response['message']
            message['subject'] = "Notification Status"
            check_in.notification_text = timezone.now()
            check_in.save()
        # Notification text failed to send
        elif not response['success']:
            message['body'] = "Unknown Error. You'll need to manually notify customer " + check_in.phone_number
            message['subject'] = "Failed to Notify Customer"

    open_check_ins = list(Checkin.waiting.all())

    data = {'message': [message], 'check_ins': open_check_ins}
    return JsonResponse(data, safe=False)


# handles employee manually cancelling checkin from dashboard view
def cancel_checkin(request):
    pk = request.GET['pk']
    check_in = get_object_or_404(Checkin, pk=pk)
    check_in.canceled = True
    check_in.save()
    open_check_ins = list(Checkin.waiting.all())

    message = {'body': "Checkin Cancelled for " + check_in.phone_number, 'subject': 'Cancellation Notice'}
    data = {'message': [message], 'check_ins': open_check_ins}
    return JsonResponse(data, safe=False)


# create table to keep track of twilio webhook calls
@csrf_exempt
@require_POST
def twilio_webhook(request):
    json_data = request.POST
    # print(json.dumps(json_data, indent=4, sort_keys=True))
    received_sms = json_data['Body']
    from_number = json_data['From']

    # creates database record of incoming message
    twilio_message = TwilioMessages(incoming_message_sid=json_data['MessageSid'], body=received_sms,
                                    phone_number=from_number, status=json_data['SmsStatus'],
                                    type='incoming_message')
    twilio_message.save()

    process_received_sms(from_number, received_sms)
    return HttpResponse(status=200)


@csrf_exempt
@require_POST
def twilio_status(request):
    json_data = request.POST
    # print(json.dumps(json_data, indent=4, sort_keys=True))

    sid = json_data['MessageSid']
    message_status = json_data['MessageStatus']
    to_number = json_data['To']

    twilio_message = get_object_or_404(TwilioMessages, sent_message_sid=sid)
    twilio_message.status = message_status
    twilio_message.save()

    return HttpResponse(status=200)
