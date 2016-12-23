"""
Testing Users Endpoint
"""

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase

from plugs_core import utils
from plugs_core.testcases import PlugsAPITestCase

from plugs_auth.tests.factories import UserFactory

model = get_user_model()

class TestViews(PlugsAPITestCase):
    """
    Testing Views
    """

    def test_guest_can_activate_account(self):
        """
        Ensures guest can activate account
        """
        # setup
        # user = UserFactory(is_active=True)
        user = UserFactory(is_active=False, first_name='Joe')

        # @FIX url pattern not correct
        url = reverse('activate-user') + '?token=' + user.token

        # exercise
        response = self.client.get(url)

        # assert
        self.assert200(response)
        self.assertEqual(model.objects.get(pk=user.pk).is_active, True)
        self.assertEqual(response.data, { "message": "Activated"})


    def test_guest_can_start_reset_password_process(self):
        """
        Ensures guest can start reset password process
        """
        # setup
        user = UserFactory(is_active=True)

        # exercise
        url = reverse('reset-password')
        data = {'email': user.email}
        response = self.client.post(url, data)
        self.assert200(response)

        # assert validation token has been refreshed
        new_token = model.objects.get(pk=user.pk).token
        self.assertNotEqual(user.token, new_token)


    def test_guest_can_set_new_password(self):
        """
        Ensures guest can set new password
        """
        # setup
        user = UserFactory(is_active=True)

        # exercise
        data = {
            'email': user.email,
            'token': user.token,
            'password': 'newpassword'
        }

        self.client.post(reverse('set-password'), data)
        self.assertLogin(user.email, 'newpassword')


    def test_inactive_user_can_reset_password_and_login(self):
        """
        Ensures inactive user can reset password and login
        """
        user = UserFactory(is_active=False)

        # exercise
        data = {'email': user.email}
        response = self.client.post(reverse('reset-password'), data)
        self.assert200(response)

        user.refresh_from_db()

        # exercise
        data = {
            'email': user.email,
            'token': user.token,
            'password': 'newpassword'
        }
        response = self.client.post(reverse('set-password'), data)
        self.assert200(response)

        user.refresh_from_db()

        # assert
        self.assert200(response)
        self.assertLogin(user.email, 'newpassword')
        self.assertEqual(user.is_active, True)


    def test_guest_cannot_set_new_password_without_token(self):
        """
        Ensures guest cannot set new password without token
        """
        # setup
        user = UserFactory(is_active=True)

        # exercise
        data = {
            'email': user.email,
            'password': 'newpassword'
        }

        response = self.client.post(reverse('set-password'), data)
        self.assert400(response)
        self.assertCannotLogin(user.email, 'newpassword')


    def test_guest_cannot_set_new_password_with_invalid_token(self):
        """
        Ensures guest cannot set new password with invalid token
        """
        # setup
        user = UserFactory(is_active=True)

        # exercise
        data = {
            'email': user.email,
            'password': 'newpassword',
            'token': 'xxx'
        }

        response = self.client.post(reverse('set-password'), data)
        self.assert404(response)
        self.assertCannotLogin(user.email, 'newpassword')
