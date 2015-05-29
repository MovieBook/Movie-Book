from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^index/', views.login, name='login'),
    url(r'^authenticate/$', views.auth_view, name='authenticate'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^home/$', views.home, name='logged'),
    url(r'^invalid/$', views.invalid_login, name='invalid_login'),
    url(r'^register/$', views.register_user, name='register'),
    url(r'^register_success/$',
        views.register_success, name='register_success'),
    url(r'^about/$', views.about, name='about'),
    url(r'^favourites/$', views.favourites, name='favourites'),
    # url(r'^movies/$', views.get_movies, name="movies")
]
