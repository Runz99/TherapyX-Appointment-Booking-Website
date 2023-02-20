from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

TIME_SLOTS = (
    ('10:00 AM','10:00 AM'),
    ('11:00 AM','11:00 AM'),
    ('12:00 AM','12:00 AM'),
    ('2:00 PM','2:00 PM'),
    ('3:00 PM','3:00 PM'),
    ('4:00 PM','4:00 PM'),
    ('6:00 PM','6:00 PM'),
    ('7:00 PM','7:00 PM'),
    ('8:00 PM','8:00 PM'),
)

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    day = models.DateField(default=datetime.now)
    time = models.CharField(max_length=10, choices=TIME_SLOTS, default="8:00 PM")
    time_booked = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return f"{self.user.username} | day: {self.day} | time: {self.time}"