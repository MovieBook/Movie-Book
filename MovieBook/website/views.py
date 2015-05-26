from django.shortcuts import render_to_response, redirect, render
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseNotFound
from django.http import Http404
from bs4 import BeautifulSoup
import json
import requests

def get_id(name):
    api_key = '&api_key=8f5d9e5ae1a7b93ba0d76d621a742501'
    title = name
    result = requests.get(
        'http://api.themoviedb.org/3/search/movie?query=' + title
        + api_key
    )
    result = result.json()
    dict_of_movies = dict()
    for el in result["results"]:
        dict_of_movies[el["title"]] = el["id"]
        return dict_of_movies[el["title"]]


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


def get_info(id):
    movie_id = str(id)
    info_request = requests.get("http://api.themoviedb.org/3/movie/{}?api_key=8f5d9e5ae1a7b93ba0d76d621a742501".format(movie_id))
    diction = info_request.json()
    new_dict = {}
    string = ""
    for elem in ["title","original_title", "runtime", "genres", "release_date", "overview", "status", "vote_average"]:
        if elem == "vote_average":
            new_dict["rating"] = diction[elem]
        elif elem == "genres":
            for x in diction[elem]:
                string += x['name']
                string += " "
            new_dict[elem] = string
        else:
            new_dict[elem] = diction[elem]
    return new_dict


def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('login.html', c)


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
        movie_name = request.POST.get("text")
        movie_id = get_id(movie_name)
        movie_info = get_info(movie_id)
        movie_trailer = get_trailer(movie_name)
        return render(request, "favourites.html", locals())
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


@require_http_methods(["GET", "POST"])
def favourites(requests):
    return render_to_response("favourites.html")
