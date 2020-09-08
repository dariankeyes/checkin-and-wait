from django.contrib import admin
from . models import Checkin, Reason, TextMessage, Word


class CheckinAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'name', 'notification_text', 'canceled', 'checkin_time']


admin.site.register(Checkin, CheckinAdmin)
admin.site.register(Reason)
admin.site.register(TextMessage)
admin.site.register(Word)
