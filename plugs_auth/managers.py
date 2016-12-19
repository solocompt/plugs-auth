"""
Plugs Authentication Managers
"""

from django.contrib.auth.models import BaseUserManager


class PlugsAuthManager(BaseUserManager):
    """
    Custom manager, the parent class provides
    some utils to manage users, like normalize_email
    and make_random_password
    """
    
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    
    def create(self, email, password=None, silent=False, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user = self._create_user(email, password, **extra_fields)
        if not silent:
            user.send_activation_email()
        return user

    
    def create_superuser(self, email, password, **extra_fields):
        """
        This method is provided to enable createsuperuser command
        a superuser is automatically made staff and active
        """
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
