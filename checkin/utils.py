from .models import Checkin


# gets a list of check_ins that are waiting for assistance
def currently_waiting():
    check_ins = list(Checkin.objects.filter(notification_text=None, canceled=None).values('name', 'phone_number',
                                                                                          'checkin_time', 'pk',
                                                                                          'reason__reason'))
    return check_ins