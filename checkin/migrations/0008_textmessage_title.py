# Generated by Django 2.1 on 2020-08-26 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkin', '0007_textmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='textmessage',
            name='title',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
