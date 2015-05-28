from django.shortcuts import render_to_response, redirect, render
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseNotFound
from django.http import Http404
from bs4 import BeautifulSoup
from .models import Movie, Actor, Genre
from django.http import *
from django.template import RequestContext

import socket
import json
import requests


def get_imdb_info(name):
    api_key = '&api_key=8f5d9e5ae1a7b93ba0d76d621a742501'
    title = name
    result = requests.get(
        'http://api.themoviedb.org/3/search/movie?query=' + title
        + api_key
    )

    result = result.json()
    info = []
    if 'results' in result.keys():
        for el in result["results"]:
            info.append({"id": el["id"], "cover": el['poster_path']})
        return info
    raise Http404("Няма зададен филм!")


def get_trailer(nam):
    api_key = 'AIzaSyD4eZKe1HehOtJ7LVTqDjhKqnA2JpNzWSE'
    title = nam
    result = requests.get(
        'https://www.googleapis.com/youtube/v3/search?part=id&maxResults=1&q='
        + title
        + 'trailer&type=video&videoEmbeddable=true&key='
        + api_key
    )
    result = result.json()
    all_items = result["items"]
    movie_trailer_id = all_items[0]['id']['videoId']
    link_to_trailer = 'https://www.youtube.com/embed/' + movie_trailer_id
    return link_to_trailer


def get_cool_movie_info(id):
    print(id)
    info = {}
    info_request = requests.get("http://api.themoviedb.org/3/movie/{}?api_key=8f5d9e5ae1a7b93ba0d76d621a742501".format(str(id)))
    result = info_request.json()
    if result['title']:
        allowed_keys = ["title","original_title", "runtime", "genres", "release_date", "overview", "status", "vote_average"]
        info = {k: v for k, v in result.items() if k in allowed_keys}
        genres = ""

        for x in info["genres"]:
            genres += x['name']
            genres += ", "
        genres = genres[:len(genres) - 2]

        info['genres'] = genres
        info['rating'] = info['vote_average']
        del info['vote_average']

        IMAGE_URL = 'http://image.tmdb.org/t/p/w500'
        url_to_img = IMAGE_URL + str(result['poster_path'])
        info['cover'] = url_to_img
    return info


def get_cast_info(id):
    api_key = 'api_key=8f5d9e5ae1a7b93ba0d76d621a742501'
    result = requests.get(
        'http://api.themoviedb.org/3/movie/'
        + id
        + '/casts?'
        + api_key
    )
    stars = ""
    for el in result.json()['cast']:
        stars += el['name']
        stars += ", "
    stars = stars[:len(stars) - 2]
    return stars


def get_info(id, namemovie):
    cool_info = get_cool_movie_info(id)
    if not cool_info:
        raise Http404("Не съществува такъв филм!")
    cast_info = get_cast_info(id)

    cool_info['stars'] = cast_info
   
    cool_info["trailer"] = get_trailer(namemovie)
    
    return json.dumps(cool_info)


def main(request):
   return render_to_response('favourites.html', context_instance=RequestContext(request))

def ajax(request):
    if request.POST.has_key('client_response'):
        x = request.POST['client_response']
        y = socket.gethostbyname(x)
        response_dict = {}
        response_dict.update({'server_response': y})
        return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
    else:
        response_dict =  {"err" : "Oooops"}
        return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')

def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('login.html', c)


def add_movie(t, ov, rat, le, rel_d, st, orig_t, c, tr):
    m = Movie(title=t, overview=ov, rating=str(rat), length=str(le), release_date=rel_d, status=st, original_title=orig_t, cover=c, trailer=tr)
    m.save()


def movie_check(t, movie_info):
    m = Movie.objects.filter(title=t)
    count = 0
    for i in m:
        count += 1
    if count == 0:
        add_movie(movie_info['title'], movie_info['overview'], movie_info['rating'], movie_info['runtime'], movie_info['release_date'], movie_info['status'], movie_info['original_title'], movie_info['cover'], movie_info['trailer'])
    else:
        return m

def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return redirect('website:logged')
    else:
        return redirect('website:invalid_login')


@login_required(login_url="website:login")
def home(request):
    if request.POST:
        return redirect('website:favourites')
    else:
        c = {}
        c.update(csrf(request))
        return render_to_response('loggedin.html', c)


def invalid_login(request):
    return render_to_response('invalid_login.html')


def logout(request):
    auth.logout(request)
    return render_to_response('logout.html')


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render_to_response('register_success.html')
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()

    return render_to_response('register.html', args)


def register_success(request):
    return render_to_response('register_success.html')


def about(request):
    return render_to_response('about.html')


@require_http_methods("POST")
def get_movies(request):
    if request.POST:
        movie_name = request.POST.get("text")
        movie_imdb_info = get_imdb_info(movie_name)
        movies_data = {}
        for imdb_movie in movie_imdb_info:
            id = str(imdb_movie['id'])
            cover = imdb_movie['cover']
            movie_data = {}
            movie_data['info'] = get_info(id, movie_name)
            movie_data['trailer'] = get_trailer(movie_name)
            movie_data['cover'] = cover
            movies_data[id] = movie_data

        return HttpResponse(json.dumps(movies_data), mimetype='application/javascript')
    else:
        response_dict =  {"err" : "Oooops"}
        return HttpResponse(json.dumps(response_dict), mimetype='application/javascript')

@require_http_methods("POST")
def favourites(request):
    print("blah")