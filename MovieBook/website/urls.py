from django.conf.urls import url, patterns
#from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('website.views',
    url(r'^$', 'register_user'),
    url(r'^/$', 'register_user'),
    url(r'^login/$',  'login'),
    url(r'^auth/$',  'auth_view'),
    url(r'^logout/$', 'logout'),
    url(r'^loggedin/$', 'loggedin'),
    url(r'^invalid/$', 'invalid_login'),
    url(r'^register/$', 'register_user'),
    url(r'^registration_success/$', 'register_success'),
    url(r'^about/$', 'about'),
    url(r'^/login/$',  'login'),
    url(r'^/auth/$',  'auth_view'),
    url(r'^/logout/$', 'logout'),
    url(r'^/loggedin/$', 'loggedin'),
    url(r'^/invalid/$', 'invalid_login'),
    url(r'^/register/$', 'register_user'),
    url(r'^/registration_success/$', 'register_success'),
    url(r'^/about/$', 'about'),
)
