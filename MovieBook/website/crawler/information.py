import requests
from pprint import pprint

film_info = {}


def get_film_title():
    film_title = input("Please enter film title: ")

    return film_title


def crawl_omdb_api_and_get_suggested_movies(title):
    response = requests.get("http://www.omdbapi.com/?s=" + title).json()

    return response["Search"]


def get_suggested_movie_titles(movies):
    titles = []

    for movie in movies:
        titles.append(movie["Title"])

    return titles


def get_real_movie_from_user(titles):
    for title in titles:
        print(title)

    movie = input("Which of this movies is your movie? ")

    return movie


def crawl_omdb_api_and_get_information_about_movie(movie):
    movie_info = requests.get("http://www.omdbapi.com/?t=" + movie).json()

    return movie_info


def main():
    user_movie = get_film_title()
    suggested_movies = crawl_omdb_api_and_get_suggested_movies(user_movie)
    titles = get_suggested_movie_titles(suggested_movies)
    real_user_movie = get_real_movie_from_user(titles)
    film_info = crawl_omdb_api_and_get_information_about_movie(real_user_movie)
    pprint(film_info)

if __name__ == '__main__':
    main()
