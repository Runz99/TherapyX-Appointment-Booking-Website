# Generated by Django 4.1.4 on 2023-02-15 10:21

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField(default=datetime.datetime.now)),
                ('time', models.CharField(choices=[('10:00 AM', '10:00 AM'), ('11:00 AM', '11:00 AM'), ('12:00 AM', '12:00 AM'), ('2:00 PM', '2:00 PM'), ('3:00 PM', '3:00 PM'), ('4:00 PM', '4:00 PM'), ('6:00 PM', '6:00 PM'), ('7:00 PM', '7:00 PM'), ('8:00 PM', '8:00 PM')], default='8:00 PM', max_length=10)),
                ('time_booked', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
