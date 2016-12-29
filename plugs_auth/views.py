"""
Plugs Auth Views
"""

from django.contrib.auth import get_user_model

from django.shortcuts import get_object_or_404
from django.conf import settings

from rest_framework import permissions
from rest_framework.decorators import list_route
from rest_framework.response import Response

from plugs_core.viewsets import CreateUpdateReadViewSet
from plugs_core.permissions import IsOwnerOrReadOnly
from plugs_auth.serializers import ResetSerializer, SetSerializer

def parse_accept_language(acceptLanguage):
    """
    Taken from:
    https://siongui.github.io/2012/10/11/python-parse-accept-language-in-http-request-header/
    """
    languages = acceptLanguage.split(",")
    locale_q_pairs = []

    for language in languages:
        if language.split(";")[0] == language:
            # no q => q = 1
            locale_q_pairs.append((language.strip(), "1"))
        else:
            locale = language.split(";")[0].strip()
            q = language.split(";")[1].split("=")[1]
            locale_q_pairs.append((locale, q))
    return locale_q_pairs


def get_languages_list():
    """
    Get the list of project supported languages
    """
    return [language[0] for language in settings.LANGUAGES]

def is_supported_language(language):
    """
    Given a language check if it belongs to the supported list
    """
    return language in get_languages_list()

def language_from_header(header):
    """
    Split the accept language header and check
    if a language preference is available in the settings
    """
    preferences = parse_accept_language(header)
    languages = get_languages_list() 
    for preference in preferences:
        # iterate over the languages setting and return the first match
        if is_supported_language(preference[0]):
            return preference[0]


def get_language_code(request, serializer):
    """
    Check request and provided data to define the user language
    """
    # first check if user provided a valid language_code
    language_code = serializer.validated_data.get('language')
    if is_supported_language('language_code'):
        return language_code
    # second check if is possible to determine the language from the
    # request headers
    try:
        accept_header = request.META['HTTP_ACCEPT_LANGUAGE']
        language_code = language_from_header(accept_header)
    # third, set the user language using the settings
    except KeyError:
        # in case the Locale Middleware is not available, use the language
        # set in the settings, the Django default is en-US
        # more information on the format used in the settings
        # http://www.i18nguy.com/unicode/language-identifiers.html
        # for now we are only using the language part of the code
        language_code = settings.LANGUAGE_CODE.split('-')[0]
    return language_code


class PlugsUserViewSet(CreateUpdateReadViewSet):
    """
    Use this in a UserViewset to make sure
    the user object lang is populated with
    language code from user submitted data,
    the request accept language header or the
    settings file

    e.g.

    class UserViewSet(PlugsUserMixin, CreateUpdateReadViewSet):
    """
    queryset = get_user_model().objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    
    def perform_create(self, serializer):
        serializer.validated_data['language'] = get_language_code(self.request, serializer)
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
    def resend_verification_email(request):
        """
        Resends the verification email to a user
        """
        kwargs = {'email': request.data.get('email'), 'is_active': False}
        user = get_object_or_404(get_user_model(), **kwargs)
        user.send_activation_email()
        return Response(data={"message": "Email sent"})
