from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase


class ProfileViewTestCase(TestCase):

    def setUp(self):
        super(ProfileViewTestCase, self).setUp()
        self.user = User.objects.create_user('test123', 'email@e.com', 'pass')
        self.client.login(username='test123',
                          password='pass')

    def test_profile_view_uses_template(self):
        response = self.client.get(reverse('view_profile', args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

