from flask_restful import Resource
from api import api
from flask import make_response, jsonify
from ..schemas import movie_schema
from ..models import movie_model
from ..services import movie_service

class MoviesList(Resource):
    #método GET: listar
    def get(self):
        movies = movie_service.get_movies()
        movieSchema = movie_schema.MovieSchema(many=True)
        return make_response(movieSchema.jsonify(movies), 200)


    
api.add_resource(MoviesList, '/movies')