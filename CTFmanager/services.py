from django.conf import settings
from requests import get


class EtherPadHelper(object):

    @staticmethod
    def create_pad(pad_name):
        """ Creates a new pad using the etherpad API running on the base_url server
        :param pad_name: etherpad pad name
        :return: succes boolean
        """
        if settings.ETHERPAD_API_KEY is not None and settings.ETHERPAD_DEFAULT_TEXT is not None \
                and settings.ETHERPAD_API_URL is not None:
            payload = {'apikey': settings.ETHERPAD_API_KEY,
                       'padID': pad_name,
                       'text': settings.ETHERPAD_DEFAULT_TEXT}
            r = get(settings.ETHERPAD_API_URL + 'createPad', params=payload)

            rj = r.json()

            return rj['code'] is 0
