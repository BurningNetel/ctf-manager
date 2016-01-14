from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone


class Event(models.Model):

    name = models.CharField(primary_key=True, max_length=20, default='')
    date = models.DateTimeField(default='')

    def get_absolute_url(self):
        return reverse('view_event', args=[self.name])

    @property
    def is_upcoming(self):
        if self.date > timezone.now():
            return True
        return False


class Challenge(models.Model):

    name = models.CharField(max_length=30, default='')
    points = models.IntegerField(default=0)
    event = models.ForeignKey(Event, default=None)