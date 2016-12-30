"""
Plugs Auth Utils
"""

from django.conf import settings

def parse_accept_language(accept_header):
    """
    Taken from:
    https://siongui.github.io/2012/10/11/python-parse-accept-language-in-http-request-header/
    """
    languages = accept_header.split(",")
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
