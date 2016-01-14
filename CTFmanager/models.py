from django.db import models
from django.utils import timezone

# Create your models here.


class Event(models.Model):

    name = models.CharField(primary_key=True, max_length=20, default='')
    date = models.DateTimeField(default='')

    @property
    def is_upcoming(self):
        if self.date > timezone.now():
            return True
        return False

