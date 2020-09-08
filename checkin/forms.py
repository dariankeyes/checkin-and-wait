from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Checkin, TextMessage


# Form used for Laptop CheckIn Page
class CheckinForm(forms.ModelForm):
    class Meta:
        model = Checkin
        fields = ('name', 'phone_number', 'reason')
        labels = {
            'name': _("Name"),
            'phone_number': _('Phone Number'),
            # 'vehicle': _('Vehicle')
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = TextMessage
        fields = '__all__'