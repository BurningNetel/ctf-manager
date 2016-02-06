from unittest.mock import patch

from django.test import TestCase

from ..models import CTFUser


class CTFUserTestCase(TestCase):

    @patch('CTFprofile.queries.ProfileQueries.get_total_score')
    def test_get_total_score_called_once(self, mock_profile_queries):
        mock_profile_queries.return_value = 0
        user = CTFUser.objects.create_user('testUser')

        score = user.total_score
        self.assertEqual(0, score)
        self.assertEqual(1, mock_profile_queries.call_count)
        self.assertIn(user.pk, mock_profile_queries.call_args[0])
