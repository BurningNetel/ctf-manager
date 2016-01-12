from django.db import models
from django.utils import timezone

# Create your models here.


class Event(models.Model):

    name = models.CharField(max_length=20, default='')
    date = models.DateTimeField(default=timezone.now)

    @property
    def is_upcoming(self):
        if self.date > timezone.now():
            return True
        return False

