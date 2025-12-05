from flask import Flask
from flask_restful import Api
from flask_pymongo import PyMongo
from flask_marshmallow import Marshmallow
#carregando flask na variavel app
app = Flask(__name__)

app.config["MONGO_URI"]= 'mongodb://localhost:27017/api-movies'

#carregando a classe api do flask restful na variavel api
api = Api(app)

mongo = PyMongo(app)

ma = Marshmallow(app)

#importando os recursos
from .resources import movie_resources