from django.contrib import admin
from . models import Checkin, Reason, TextMessage, TwilioMessages


class CheckinAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'name', 'notification_text', 'canceled', 'checkin_time']


class TwilioMessagesAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'type', 'body', 'incoming_message_sid', 'sent_message_sid', 'status']


admin.site.register(Checkin, CheckinAdmin)
admin.site.register(Reason)
admin.site.register(TextMessage)
admin.site.register(TwilioMessages, TwilioMessagesAdmin)
