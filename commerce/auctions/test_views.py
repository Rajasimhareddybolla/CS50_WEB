from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect

class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_logout_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Call the logout_view function
        response = self.client.get(reverse('logout'))

        # Check that the user is logged out
        self.assertFalse(response.context['user'].is_authenticated)

        # Check that the response is a redirect to the index page
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, reverse('index'))