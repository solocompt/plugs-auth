"""
Factory Boy Factory Definition
"""

from django.contrib.auth import get_user_model

from factory.django import DjangoModelFactory as Factory
from factory import LazyAttribute, Sequence, SubFactory


model = get_user_model()

class UserFactory(Factory):
    """
    Base User Factory
    """
    email = LazyAttribute(lambda m: '{0}@example.com'.format(m.first_name))
    first_name = Sequence(lambda n: 'User{0}'.format(n))
    last_name = 'Smith'
    token = Sequence(lambda n: 'Validation{0}'.format(n))

    # pylint: disable=R0903
    class Meta:
        """
        Metaclass Definition
        """
        model = model
