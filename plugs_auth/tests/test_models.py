"""
Testing Models
"""

from django.contrib.auth import get_user_model

from plugs_core.testcases import PlugsAPITestCase

model = get_user_model()

class TestModels(PlugsAPITestCase):
    """
    Testing Models
    """

    def test_superuser_can_login_with_new_account(self):
        """
        Ensures superuser is created and can login
        """
        data = {
            'email': 'joe@somewhere.org',
            'password': 'longandhardpass'
        }
        user = model.objects.create_superuser(**data)

        # created password should be unusable
        self.assertTrue(user.has_usable_password())
        self.assertLogin(data['email'], data['password'])
