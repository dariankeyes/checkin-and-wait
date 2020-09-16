"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('settings', views.message_config, name='settings'),
    path('terms', views.terms, name='terms'),
    path('checkin_confirmation.html/<message>', views.checkin_confirmation, name='checkin_confirmation'),
    path('get_check_ins', views.get_check_ins, name='get_check_ins'),
    path('send_ready_notification', views.send_ready_notification, name='send_ready_notification'),
    path('cancel_checkin', views.cancel_checkin, name="cancel_checkin"),
    path('twilio_webhook', views.twilio_webhook, name='twilio_webhook'),
    path('twilio_status', views.twilio_status, name='twilio_status')
]
