"""
Email Template Definition
"""

from urllib.parse import urlencode

from plugs_mail.mail import PlugsMail

from plugs_auth.settings import plugs_auth_settings as settings


class ActivateAccount(PlugsMail):
    """
    Email sent to user after registration with link to activate his account
    """
    template = 'ACTIVATE_ACCOUNT'
    context = ('User', )
    description = 'Email sent to user after registration with link to activate his account'

    def get_extra_context(self):
        user = self.context_data.get('user')
        params = '?' + urlencode({
            'token': user.token
        })
        activate_uri = settings['SITE_ACTIVATE_VIEW'] + params
        return {'activate_uri': activate_uri}


class ResetPassword(PlugsMail):
    """
    Email sent to user with reset password link
    """
    template = 'RESET_PASSWORD'
    context = ('User', )
    description = 'Email sent to user with reset password link'

    def get_extra_context(self):
        """
        Adds reset_password_uri as extra context
        """
        user = self.context_data.get('user')

        params = '?' + urlencode({
            'email': user.email,
            'token': user.token
        })

        reset_password_uri = settings['SITE_RESET_VIEW'] + params
        return {'reset_password_uri': reset_password_uri}


class AccountActivated(PlugsMail):
    """
    Email sent to user after succesful account activation
    """
    template = 'ACCOUNT_ACTIVATED'
    context = ('User', )
    description = 'Email sent to user after succesful account activation'
