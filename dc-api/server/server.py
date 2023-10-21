# Copyright (C) 2023 Borello Benjamin
# server/server.py
import os
from typing import Dict
from dal import DAL
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from models.movie import Movie
from server import route_get_movie, route_post_movie


# todo(nmj): move status const into an other script
# todo(nmj): write all status variables
STATUS_200 = {
    "code": 200,
    "message": "OK - The requested action was successful."
}
STATUS_201 = {
    "code": 201,
    "message": "Created - A new resource was created."
}
STATUS_400 = {
    "code": 400,
    "message": "Bad Request - The request was malformed."
}
STATUS_404 = {
    "code": 404,
    "message": "Not Found - The requested resource was not found."
}


# Create Flask application
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def RunServer() -> None:
    if (os.environ.get('ENV') == 'production'):
        # todo(nmj): Handle production environment
        app.run()
    else:
        app.run(host='0.0.0.0', port=8080, debug=True)


# Route "/api/movie/<id_movie>" (GET) return movie with the given id
@app.route('/api/movie/<int:id_movie>/<string:option>', methods=['GET'])
@cross_origin()
def get_movie(id_movie, option):
    print(f"[DC-api] ['GET' /api/movie/{id_movie}]/{option} Requesting movie from database...")

    response = {
        "status": {},
        "movie": None 
    }

    if (not option in ["minimal", "details"]):
        print(f"[DC-api] ['GET' /api/movie/{id_movie}]/{option} Unknown option")
        response["status"] = STATUS_400
        return jsonify(response)

    movie: Dict = route_get_movie.GetMovie(id_movie, option)

    response["movie"] = movie
    if (movie):
        print(f"[DC-api] ['GET' /api/movie/{id_movie}]/{option} Movie request successfuly.")
        response["status"] = STATUS_200
    else:
        print(f"[DC-api] ['GET' /api/movie/{id_movie}]/{option} Movie request failed.")
        response["status"] = STATUS_404

    return jsonify(response)



# Route "/api/movie" (POST) create || update movie
# todo(nmj): return relevant response to FirCinema to display it in the extension
@app.route('/api/movie', methods=['POST'])
@cross_origin()
def post_movie():
    if not request.json or not 'title' in request.json:
        return jsonify({'error': 'Title is required'}), 400

    route_post_movie.ApplyData(request.json)

    response = {
        "status": STATUS_201,
        "request.json": request.json,
    }

    return jsonify(response)
