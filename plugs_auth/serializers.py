"""
Custom authentication serializers
"""

from rest_framework import serializers


class ResetSerializer(serializers.Serializer):
    """
    Custom serializer to use with reset_password api view
    """
    email = serializers.EmailField()


class SetSerializer(serializers.Serializer):
    """
    Custom serializer to use with set_password api view
    """
    email = serializers.EmailField()
    password = serializers.CharField()
    token = serializers.CharField()
