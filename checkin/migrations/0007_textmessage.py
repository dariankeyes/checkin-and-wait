# Generated by Django 2.1 on 2020-08-26 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkin', '0006_checkin_vehicle'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(blank=True, max_length=120, null=True)),
            ],
        ),
    ]
