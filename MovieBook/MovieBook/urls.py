from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$',  'website.views.login'),
    url(r'^accounts/auth/$',  'website.views.auth_view'),
    url(r'^accounts/logout/$', 'website.views.logout'),
    url(r'^accounts/loggedin/$', 'website.views.loggedin'),
    url(r'^accounts/invalid/$', 'website.views.invalid_login'),
    url(r'^accounts/register/$', 'website.views.register_user'),
    url(r'^accounts/register_success/$', 'website.views.register_success'),
    url(r'^about/$', 'website.views.about'),
]
