from django.shortcuts import render_to_response, redirect, render
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseNotFound
from .models import Movie
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


def get_cast(id, namemovie):
    movie_id = str(id)
    info_request = requests.get(
        "http://api.themoviedb.org/3/movie/{}?api_key=8f5d9e5ae1a7b93ba0d76d621a742501".format(movie_id))
    diction = info_request.json()
    string = ""
    api_key = 'api_key=8f5d9e5ae1a7b93ba0d76d621a742501'
    result = requests.get(
        'http://api.themoviedb.org/3/movie/'
        + movie_id
        + '/casts?'
        + api_key
    )
    result = result.json()
    stars = ""
    if 'title' in diction.keys():
        allowed_keys = ["title", "original_title", "runtime", "genres",
                        "release_date", "overview", "status", "vote_average"]
        diction1 = {k: v for k, v in diction.items() if k in allowed_keys}
        for el in result['cast']:
            stars += el['name']
            stars += ", "
        stars = stars[:len(stars) - 2]
    return stars


def get_info(id, namemovie):
    movie_id = str(id)
    info_request = requests.get(
        "http://api.themoviedb.org/3/movie/{}?api_key=8f5d9e5ae1a7b93ba0d76d621a742501".format(movie_id))
    diction = info_request.json()
    string = ""
    api_key = 'api_key=8f5d9e5ae1a7b93ba0d76d621a742501'
    result = requests.get(
        'http://api.themoviedb.org/3/movie/'
        + movie_id
        + '/casts?'
        + api_key
    )
    result = result.json()
    stars = ""
    if 'title' in diction.keys():
        allowed_keys = ["title", "original_title", "runtime", "genres",
                        "release_date", "overview", "status", "vote_average"]
        diction1 = {k: v for k, v in diction.items() if k in allowed_keys}
        for el in result['cast']:
            stars += el['name']
            stars += ", "
        stars = stars[:len(stars) - 2]
        diction1['stars'] = stars
        for x in diction1["genres"]:
            string += x['name']
            string += ", "
        string = string[:len(string) - 2]
        diction1['genres'] = string
        diction1['rating'] = diction1['vote_average']
        del diction1['vote_average']
        diction1["trailer"] = get_trailer(namemovie)
        IMAGE_URL = 'http://image.tmdb.org/t/p/w500'
        url_to_img = IMAGE_URL + diction['poster_path']
        diction1['cover'] = url_to_img
        # json1 = json.dumps(diction1)
        return diction1
    else:
        raise Http404("Не съществува такъв филм!")


def add_movie(t, ov, rat, le, rel_d, st, orig_t, c, tr, g, a):
    m = Movie(title=t, overview=ov, rating=str(rat), length=str(le), release_date=rel_d, status=st, original_title=orig_t, cover=c, trailer=tr, genres=g, actors=a)
    m.save()


def movie_check(t, movie_info):
    m = Movie.objects.filter(title=t)
    count = 0
    for i in m:
        count += 1
    if count == 0:
        add_movie(movie_info['title'], movie_info['overview'], movie_info['rating'], movie_info['runtime'], movie_info['release_date'], movie_info['status'], movie_info['original_title'], movie_info['cover'], movie_info['trailer'], movie_info['genres'], movie_info['stars'])
    else:
        return m


def check_db_for_movie(movname):
    mov = Movie.objects.filter(title__iexact=movname)
    count = 0
    for i in mov:
        count += 1
    if count == 0:
        return False
    else:
        return mov


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
        return redirect('website:movies')
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


def movie_info_db(movie):
    movie_dict = {}
    movie_dict['title'] = movie.title
    movie_dict['original_title'] = movie.original_title
    movie_dict['runtime'] = movie.length
    movie_dict['genres'] = movie.genres
    movie_dict['stars'] = movie.actors
    movie_dict['release_date'] = movie.release_date
    movie_dict['overview'] = movie.overview
    movie_dict['status'] = movie.status
    movie_dict['vote_average'] = movie.rating
    movie_dict['cover'] = movie.cover
    return movie_dict


@require_http_methods("POST")
def movies(request):
    if request.POST:
        movie_name = request.POST.get("text")
        db_movie = check_db_for_movie(movie_name)
        if not db_movie:
            movie_id = get_id(movie_name)
            movie_info = get_info(movie_id, movie_name)
            movie_trailer = get_trailer(movie_name)
            movie_add = movie_check(movie_info['title'], movie_info)
            movie_cover = movie_info['cover']
        else:
            #movie_id = db_movie.id
            movie_info = movie_info_db(db_movie[0])
            movie_trailer = get_trailer(movie_info['title'])
            movie_cover = movie_info['cover']

        return render(request, "favourites.html", locals())
    else:
        raise Http404("PAGE DOES NOT EXISTS")
