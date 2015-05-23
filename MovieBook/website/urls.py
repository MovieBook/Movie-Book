from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^accounts/login/$', views.login, name='login'),
    url(r'^accounts/auth/$', views.auth_view, name='authenticate'),
    url(r'^accounts/logout/$', views.logout, name='logout'),
    url(r'^accounts/loggedin/$', views.loggedin, name='loggedin'),
    url(r'^accounts/invalid/$', views.invalid_login, name='invalid_login'),
    url(r'^accounts/register/$', views.register_user, name='register'),
    url(r'^accounts/register_success/$',
        views.register_success, name='register_success'),
    url(r'^about/$', views.about, name='about'),
]
