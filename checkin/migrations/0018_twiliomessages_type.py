# Generated by Django 2.1 on 2020-09-15 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkin', '0017_twiliomessages'),
    ]

    operations = [
        migrations.AddField(
            model_name='twiliomessages',
            name='type',
            field=models.CharField(blank=True, choices=[('incoming_message', 'Incoming Message'), ('outgoing_message', 'Outgoing Message')], max_length=120, null=True),
        ),
    ]