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
    _pad_created = models.BooleanField(default=False)

    def _get_padname(self):
        return '%s_%s' % (self.event.name, self.name)

    @property
    def get_pad_created(self):
        return self._pad_created

    def get_absolute_etherpad_url(self):
        return settings.ETHERPAD_PAD_URL + self._get_padname()

    def get_local_pad_url(self):
        return reverse('challenge_pad', args=[self.event.name, self.name])

    def create_pad(self):
        """ Creates a new pad using the etherpad API running on the base_url server
        :return: Succes, json response
        """
        if settings.ETHERPAD_API_KEY is not None and settings.ETHERPAD_DEFAULT_TEXT is not None \
                and settings.ETHERPAD_API_URL is not None:
            payload = {'apikey': settings.ETHERPAD_API_KEY,
                       'padID': self._get_padname(),
                       'text': settings.ETHERPAD_DEFAULT_TEXT}
            r = get(settings.ETHERPAD_API_URL + 'createPad', params=payload)

            rj = r.json()

            self._pad_created = rj['code'] is 0
            return rj['code'] is 0, rj

