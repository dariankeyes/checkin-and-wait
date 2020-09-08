# Generated by Django 2.1 on 2020-09-08 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkin', '0011_auto_20200907_1439'),
    ]

    operations = [
        migrations.CreateModel(
            name='Words',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(blank=True, choices=[('check_in_words', 'Check In Words'), ('opt_in_words', 'Opt In Words'), ('opt_out_words', 'Opt Out Words'), ('help_words', 'Help Words'), ('cancel_words', 'Cancel Words')], max_length=120, null=True)),
                ('word', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='textmessage',
            name='subject',
            field=models.CharField(blank=True, choices=[('check in page', 'Check In Page'), ('ready notification', 'Ready Notification'), ('first contact', 'First Contact SMS'), ('invalid response', 'Invalid Response')], max_length=120, null=True),
        ),
    ]