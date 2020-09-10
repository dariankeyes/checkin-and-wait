from django.db import models
from django.utils import timezone
from django.db.models.functions import Lower


class Reason(models.Model):
    reason = models.CharField(max_length=120, blank=False)

    def __str__(self):
        return self.reason


# gets a list of open/waiting checkins
class WaitingCheckinManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(notification_text=None, canceled=None)\
            .values('name', 'phone_number', 'checkin_time', 'pk', 'reason__reason')


class Checkin(models.Model):
    name = models.CharField(max_length=120, blank=False)
    phone_number = models.CharField(max_length=120, blank=False)
    checkin_time = models.DateTimeField(default=timezone.now)
    notification_text = models.DateTimeField(blank=True, null=True)
    canceled = models.BooleanField(blank=True, null=True)
    reason = models.ForeignKey(Reason, on_delete=models.CASCADE, blank=True, null=True)
    vehicle = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.phone_number

    objects = models.Manager()
    waiting = WaitingCheckinManager()


# gets a text message to send
class TextManager(models.Manager):
    def get_text(self, subject):
        return super().get_queryset().filter(subject=subject).values_list('message', flat=True)[0]


class TextMessage(models.Model):
    SUBJECT_CHOICES = [
        ('check in page', 'Check In Page'),
        ('ready notification', 'Ready Notification'),
        ('first contact', 'First Contact SMS'),
        ('invalid response', 'Invalid Response'),
        ('already_checked_in_response', 'Already Checked-in Response'),
        ('cancellation_response', 'Cancellation Response'),
        ('invalid_cancellation_request', 'Invalid Cancellation Request')
    ]

    subject = models.CharField(max_length=120, choices=SUBJECT_CHOICES, blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.subject

    objects = TextManager()


# # gets a text message to send
# class WordManager(models.Manager):
#     def word_list(self, category):
#         word_list = list(Word.objects.filter(category=category).values_list(Lower('word'), flat=True))
#         return word_list
#
#
# # come back later and save the word field as lowercase text
# class Word(models.Model):
#     WORD_CATEGORIES = [
#         ('check_in_words', 'Check In Words'),
#         ('opt_in_words', 'Opt In Words'),
#         ('opt_out_words', 'Opt Out Words'),
#         ('help_words', 'Help Words'),
#         ('cancel_words', 'Cancel Words')
#     ]
#
#     category = models.CharField(max_length=120, choices=WORD_CATEGORIES, blank=True, null=True)
#     word = models.CharField(max_length=20, blank=True, null=True)
#
#     def __str__(self):
#         return self.category
#
#     objects = WordManager()
#


