"""
Test Emails
"""

from django.core.urlresolvers import reverse

from plugs_core.testcases import PlugsAPITestCase
from plugs_core import utils

from plugs_mail.management.commands import load_email_templates

from plugs_auth.tests.factories import UserFactory
from plugs_auth.settings import plugs_auth_settings


class MailTestsBoy(PlugsAPITestCase):

    def setUp(self):
        """
        Creates email templates
        """
        # uses the load email templates command to
        # auto populate our test database with email
        # templates
        command = load_email_templates.Command()
        command.handle()

    def test_email_reset_password_sent_to_user(self):
        """
        Ensures reset password email is sent to user
        """
        # setup
        user = UserFactory(is_active=False)

        # exercise
        data = {'email': user.email}
        response = self.client.post(reverse('reset-password'), data)

        self.assert200(response)
        self.assertEmailCount('Perdeste a tua password?', 1)
        self.assertEmailTo('Perdeste a tua password?', data.get('email'))

    
    def test_email_account_activated_sent_to_user(self):
        """
        Ensures account activated email is sent to user
        """
        # setup
        user = UserFactory(is_active=False)

        # @FIX url pattern not correct
        url = reverse('activate-user') + '?token=' + user.token

        response = self.client.get(url)

        # assert
        self.assert200(response)
        self.assertEmailCount('Conta ativada com sucesso', 1)
        self.assertEmailTo('Conta ativada com sucesso', user.email)

        
    def test_email_resent_verification_email(self):
        """
        Ensures user receives a new verification email
        """
        user = UserFactory(is_active=False)
        self.assertEmailCount('Ativa a tua conta', 1)

        url = reverse('resend-verification')
        data = {'email': user.email}
        
        response = self.client.post(url, data)
        self.assertEmailCount('Ativa a tua conta', 2)
        

    def test_email_resent_verification_email_not_sent_if_user_active(self):
        """
        Ensures user does not receive a new verification email if already active
        """
        user = UserFactory(is_active=True)
        self.assertEmailCount('Ativa a tua conta', 1)

        url = reverse('resend-verification')
        data = {'email': user.email}

        response = self.client.post(url, data)
        self.assertEmailCount('Ativa a tua conta', 1)
