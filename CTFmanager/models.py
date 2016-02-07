from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Min, Max
from django.utils import timezone

from .services import EtherPadHelper


class Event(models.Model):
    """
    The optional fields are: Description, Location, End_Date, Credentials, URL
    min_score, max_score
    (hidden fields): Creation_Date, Created_By
    """
    name = models.SlugField(primary_key=True, max_length=20, default='')
    date = models.DateTimeField(default='')
    description = models.TextField(default='',
                                   max_length=5000,
                                   blank=True)
    location = models.SlugField(max_length=100, default='', blank=True)
    username = models.CharField(default='', max_length=200, blank=True)
    password = models.CharField(default='', max_length=200, blank=True)
    url = models.CharField(default='', max_length=200, blank=True)
    end_date = models.DateTimeField(blank=True, null=True)
    creation_date = models.DateTimeField(default=timezone.now, blank=True)
    created_by = models.SlugField(default='Anonymous', blank=True)
    min_score = models.PositiveIntegerField(blank=True, null=True)
    max_score = models.PositiveIntegerField(blank=True, null=True)

    members = models.ManyToManyField(User)

    def join(self, user):
        if user not in self.members.all():
            self.members.add(user)
            return self.members.count()
        else:
            return -1

    def leave(self, user):
        if user in self.members.all():
            self.members.remove(user)
            return self.members.count()
        else:
            return -1

    def get_absolute_url(self):
        return reverse('view_event', args=[self.name])

    def challenge_added(self, challenge):
        if self.challenge_set.count() > 1:
            if not self.min_score and not self.max_score:
                result = self.challenge_set.aggregate(Min('points'), Max('points'))

                if not result['points__min'] is result['points__max']:
                    self.min_score = result['points__min']
                    self.max_score = result['points__max']
            else:
                chal_p = challenge.points

                if chal_p > self.max_score:
                    self.max_score = chal_p
                elif chal_p < self.min_score:
                    self.min_score = chal_p
            self.save()


    @property
    def is_upcoming(self):
        if self.date > timezone.now():
            return True
        return False


class Challenge(models.Model):
    name = models.SlugField(max_length=30, default='')
    points = models.IntegerField(default=0)
    flag = models.CharField(max_length=200, blank=True)
    event = models.ForeignKey(Event, default=None)

    _pad_created = models.BooleanField(default=False)
    solvers = models.ManyToManyField(User)

    class Meta:
        unique_together = ('name', 'event')

    def _get_padname(self):
        return '%s_%s' % (self.event.name, self.name)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Challenge, self).save(force_insert, force_update, using, update_fields)
        self.event.challenge_added(self)

    @property
    def get_pad_created(self):
        return self._pad_created

    def get_absolute_etherpad_url(self):
        return settings.ETHERPAD_PAD_URL + self._get_padname()

    def get_absolute_url(self):
        return reverse('challenge_pad', args=[self.event.name, self.name])

    def create_pad(self):
        pad_name = self._get_padname()
        self._pad_created = EtherPadHelper.create_pad(pad_name)
        return self._pad_created

    def solve(self, user):
        if user not in self.solvers.all():
            self.solvers.add(user)
            return True
        else:
            return False

