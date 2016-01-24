from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from requests import get


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

    def get_pad_url(self):
        return reverse('challenge_pad', args=[self.event.name, self.name])

    def _create_pad(self):
        """ Creates a new pad using the etherpad API running on the base_url server
        :return: Succes, json response
        """
        if settings.ETHERPAD_API_KEY is not None and settings.ETHERPAD_DEFAULT_TEXT is not None \
                and settings.ETHERPAD_BASE_URL is not None:
            padname = self.event.name + '_' + self.name
            payload = {'apikey': settings.ETHERPAD_API_KEY,
                       'padID': padname,
                       'text': settings.ETHERPAD_DEFAULT_TEXT}
            r = get(settings.ETHERPAD_BASE_URL + 'createPad', params=payload)
            rj = r.json()
            return rj['code'] is 0, rj

