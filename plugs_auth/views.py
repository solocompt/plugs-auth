"""
Authentication Views
"""

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes

from plugs_auth import serializers


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def reset_password(request):
    """
    Starts the reset password process by sending an email
    """
    serializer = serializers.ResetSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(get_user_model(), **serializer.data)
    user.set_token()
    user.send_reset_password_email()
    user.save()
    return Response(data={"message": "Email Sent"})


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def set_password(request):
    """
    Sets a new password after a reset password request
    """
    serializer = serializers.SetSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.data
    password = data.pop('password')
    user = get_object_or_404(get_user_model(), **data)
    user.password = password
    user.is_active = True  # in case the user was inactive
    user.set_token()
    user.save()
    return Response(data={"message": "New password set"})


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def activate(request):
    """
    Activates account
    """
    kwargs = {'token': request.query_params.get('token'), 'is_active': False}
    user = get_object_or_404(get_user_model(), **kwargs)
    user.is_active = True
    user.save()
    user.send_account_activated_email()
    return Response(data={"message": "Activated"})


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def resend_verification_email(request):
    """
    Resends the verification email to a user
    """
    kwargs = {'email': request.data.get('email'), 'is_active': False}
    user = get_object_or_404(get_user_model(), **kwargs)
    user.send_activation_email()
    return Response(data={"message": "Email sent"})
