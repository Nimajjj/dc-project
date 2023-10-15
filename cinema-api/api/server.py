# api/server.py
import os
from dal import DAL
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from models import movie

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
        app.run()
    else:
        load_dotenv() # Load .env file if not in production environment
        app.run(host='0.0.0.0', port=8080, debug=True)


# Route "/api/movie/<id_movie>" (GET) return movie with the given id
@app.route('/api/movie/<int:id_movie>', methods=['GET'])
def get_movie(id_movie):
    dal = DAL()
    query = f"SELECT * FROM movies WHERE id_movie={id_movie}"

    results = dal.SelectSingleRow(query)
    
    response = {
        "status": {},
        "movie": results,
    }

    response["status"] = STATUS_200 if (results != None) else STATUS_204

    return jsonify(response)



# Route "/api/movie" (POST) create || update movie
@app.route('/api/movie', methods=['POST'])
@cross_origin()
def post_movie():
    if not request.json or not 'title' in request.json:
        return jsonify({'error': 'Title is required'}), 400

    m = movie.Movie(
        0,
        request.json["duration"],
        "",
        "",
        request.json["title"],
        request.json["overview"],
        request.json["thumbnail"],
        request.json["date"],
        request.json["visa"],
        0,
        "",
        "",
        ""
    )                                           # movie.Movie
    distributor = request.json["distributor"]   # str
    language = request.json["language"]         # list
    country = request.json["country"]           # list
    genres = request.json["genres"]             # list
    actors = request.json["actors"]             # list
    directors = request.json["directors"]       # list
    writers = request.json["writers"]           # list

    print(m)               
    print(distributor)     
    print(language)
    print(country)
    print(genres)
    print(actors)
    print(directors)
    print(writers) 

    response = {
        "status": STATUS_201,
        "request.json": request.json,
    }
    return jsonify(response)
