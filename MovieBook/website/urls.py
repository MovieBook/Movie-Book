from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^authenticate/$', views.auth_view, name='authenticate'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^loggedin/$', views.loggedin, name='logged'),
    url(r'^invalid/$', views.invalid_login, name='invalid_login'),
    url(r'^register/$', views.register_user, name='register'),
    url(r'^register_success/$',
        views.register_success, name='register_success'),
    url(r'^about/$', views.about, name='about'),
]
