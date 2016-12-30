"""
Plugs Auth Views
"""

from django.contrib.auth import get_user_model

from django.shortcuts import get_object_or_404

from rest_framework import permissions
from rest_framework.decorators import list_route
from rest_framework.response import Response

from plugs_core.viewsets import CreateUpdateReadViewSet

from plugs_auth.serializers import ResetSerializer, SetSerializer
from plugs_auth import utils


class PlugsUserViewSet(CreateUpdateReadViewSet):
    """
    Use this class as a base class for a user viewset,
    this class provides activate, reset_password, set_password,
    resend_verification_email and populates the user object with
    the language using user submited data, accept-language header
    or project settings
    """
    
    def perform_create(self, serializer):
        serializer.validated_data['language'] = utils.get_language_code(self.request, serializer)
        serializer.save()

    @list_route(methods=['GET'], permission_classes=[permissions.AllowAny])
    def activate(self, request):
        kwargs = {'token': request.query_params.get('token'), 'is_active': False}
        user = get_object_or_404(get_user_model(), **kwargs)
        user.is_active = True
        user.save()
        user.send_account_activated_email()
        return Response(data={"message": "Activated"})

    @list_route(methods=['POST'], permission_classes=[permissions.AllowAny])
    def reset_password(self, request):
        """
        Starts the reset password process by sending an email
        """
        serializer = ResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(get_user_model(), **serializer.data)
        user.set_token()
        user.send_reset_password_email()
        user.save()
        return Response(data={"message": "Email Sent"})

    @list_route(methods=['POST'], permission_classes=[permissions.AllowAny])
    def set_password(self, request):
        """
        Sets a new password after a reset password request
        """
        serializer = SetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        password = data.pop('password')
        user = get_object_or_404(get_user_model(), **data)
        user.password = password
        user.is_active = True  # in case the user was inactive
        user.set_token()
        user.save()
        return Response(data={"message": "New password set"})

    @list_route(methods=['POST'], permission_classes=[permissions.AllowAny])
    def resend_verification_email(self, request):
        """
        Resends the verification email to a user
        """
        kwargs = {'email': request.data.get('email'), 'is_active': False}
        user = get_object_or_404(get_user_model(), **kwargs)
        user.send_activation_email()
        return Response(data={"message": "Email sent"})
