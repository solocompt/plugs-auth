from django.conf.urls import url

from plugs_core import utils

from plugs_auth.settings import plugs_auth_settings
from plugs_auth import views

endpoint = plugs_auth_settings['USER_ENDPOINT']

urlpatterns = [
    url(endpoint + r'/reset_password/$', views.reset_password, name='reset-password'),
    url(endpoint + r'/set_password/$', views.set_password, name='set-password'),
    url(endpoint + r'/activate/$', views.activate, name='activate-user'),
    url(endpoint + r'/resend_verification_email/$', views.resend_verification_email, name='resend-verification'),
]
