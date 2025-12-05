from api import mongo 
from ..models import movie_model

#Função para cadastrar
def add_movie(movie):
    mongo.db.movies.insert_one({
        'title': movie.title,
        'description': movie.description,
        'year': movie.year,
        'duration': movie.duration
    })

def get_movies():
    return list(mongo.db.movies.find())