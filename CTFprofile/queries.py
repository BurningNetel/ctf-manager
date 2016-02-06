from django.contrib.auth.models import User


class ProfileQueries(object):

    @staticmethod
    def get_total_score(pk):
        """  Calculates the users total score
        :param pk: primary key of an user
        :return: the total score count.
        """
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise ValueError("unknown private key")

        count = 0

        for challenge in user.challenge_set.all():
            count += challenge.points

        return count
