from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api_redirect', views.api_redirect, name='api_redirect')
]