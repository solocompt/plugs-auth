from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth import hashers

from plugs_core import utils
from plugs_mail import utils as mail_utils

from plugs_auth import emails
from plugs_auth.managers import PlugsAuthManager

class PlugsAuthModel(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    token = models.CharField(max_length=24, null=False, unique=True)
    language = models.CharField(max_length=2, default='en')
    objects = PlugsAuthManager()

    # the field used to authenticate a user
    USERNAME_FIELD = 'email'

    def __init__(self, *args, **kwargs):
        super(PlugsAuthModel, self).__init__(*args, **kwargs)
        self.__original_password = self.password

    @property
    def username(self):
        return self.USERNAME_FIELD

    def set_token(self):
        params = {'length': 24}
        queryset = self.__class__.objects
        self.token = utils.get_db_distinct(queryset, 'token', utils.random_string, **params)

    def send_reset_password_email(self):
        """
        Send email to user with reset password link
        """
        mail_utils.to_email(emails.ResetPassword, self.email, self.language, **{'user': self})

    def send_activation_email(self):
        """
        Send email to user with activation details
        """
        mail_utils.to_email(emails.ActivateAccount, self.email, self.language, **{'user': self})

    def send_account_activated_email(self):
        """
        Send email to user saying account has been activated
        """
        mail_utils.to_email(emails.AccountActivated, self.email, self.language,  **{'user': self})

    def is_password_hashed(self):
        try:
            return hashers.identify_hasher(self.password)
        except ValueError:
            return False

    def _update_password(self):
        if not self.is_password_hashed():
            self.set_password(self.password)

    def password_has_changed(self):
        return self.password != self.__original_password


    def save(self, *args, **kwargs):
        if self.pk and self.password_has_changed():
            self._update_password()
        else:
            self.set_token()
        super(PlugsAuthModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
