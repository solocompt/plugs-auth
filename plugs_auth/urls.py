from django.conf.urls import url

from plugs_core import utils

from plugs_auth import views

endpoint = utils.get_authentication_endpoint()

urlpatterns = [
    url(r'^' + endpoint + r'/reset_password/$', views.reset_password),
    url(r'^' + endpoint + r'/set_password/$', views.set_password),
    url(r'^' + endpoint + r'/activate/$', views.activate),
    url(r'^' + endpoint + r'/resend_verification_email/$', views.resend_verification_email),
]
