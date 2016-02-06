from django.contrib.auth.models import User

from CTFprofile.queries import ProfileQueries


class CTFUser(User):

    class Meta:
        proxy = True

    @property
    def total_score(self):
        return ProfileQueries.get_total_score(self.pk)
