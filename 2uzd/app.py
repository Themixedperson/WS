from flask import Flask
from redis import Redis
from flask import jsonify
from flask import request
import requests
import json
import re
import copy
app = Flask(__name__)
movies = [ {
                        'ID' : '0',
                        'Title' : 'Avengers: Infinity War',
                        'Release_date' : '05-2018',
                        'Rating' : '5.3',
                        'Genre' : 'Fantasy',
			'Album_ID' : '1'
                   },
                   {
                        'ID' : '1',
                        'Title' : 'Avengers: Infinity War',
                        'Release_date' : '05-2018',
                        'Rating' : 'Not Rated',
                        'Genre' : 'Fantasy',
			'Album_ID' : '1'
                   },
                   {
                        'ID' : '2',
                        'Title' : 'Movie_1',
                        'Release_date' : '05-2018',
                        'Rating' : '8.0',
                        'Genre' : 'Fantasy',
			'Album_ID' : '1'
                   },
                   {
                        'ID' : '3',
                        'Title' : 'Movie_2',
                        'Release_date' : '05-2018',
                        'Rating' : '3.75',
                        'Genre' : 'Fantasy',
			'Album_ID' : '1'
                   },
                   {
                        'ID' : '4',
                        'Title' : 'Movie_3',
                        'Release_date' : '05-2018',
                        'Rating' : 'Not Rated',
                        'Genre' : 'Fantasy',
			'Album_ID' : '1'
                   },
                   {
                        'ID' : '5',
                        'Title' : 'Avengers: Infinity War',
                        'Release_date' : '05-2018',
                        'Rating' : 'Not Rated',
                        'Genre' : 'Fantasy',
			'Album_ID' : '1'
                   },
                   {
                        'ID' : '6',
                        'Title' : 'Alpha',
                        'Release_date' : '09-2018',
                        'Rating' : 'Not Rated',
                        'Genre' : 'Fantasy',
			'Album_ID' : '1'
                   },
                   {
                        'ID' : '7',
                        'Title' : 'Fantastic Beasts: Crimes of Grundelvald',
                        'Release_date' : '11-2018',
                        'Rating' : 'Not Rated',
                        'Genre' : 'Fantasy',
			'Album_ID' : '1'
                   },
                   {
                        'ID' : '8',
                        'Title' : 'Insidious: the last key',
                        'Release_date' : '01-2018',
                        'Rating' : 'Not Rated',
                        'Genre' : 'Horror',
			'Album_ID' : '1'
                  }]

@app.route('/movies', methods=['GET'])
def hello():
	if( request.args.get('embedded', '') == "album"):
		moviesEmb=copy.deepcopy(movies)
		for i in range(0, len(movies)):
			try:
				r = requests.get('http://web1:81/albums/'+moviesEmb[int(i)]['Album_ID'])
				r = json.loads(r.text)
				moviesEmb[int(i)]['Album'] = r[0]
			except:
				moviesEmb[int(i)]['Album'] = "null"
		return jsonify(moviesEmb), 200
	elif( request.args.get('title', '')):
		foundMovies = []
		for i in movies:
			if( re.search(request.args.get('title', ''), i["Title"], re.IGNORECASE)):
				foundMovies.append(i)
		return jsonify(foundMovies), 200
	elif( request.args.get('genre', '')):
		foundMovies = [ movie for movie in movies if (movie['Genre'] == request.args.get('genre', ''))]
		return jsonify(foundMovies), 200
	elif( request.args.get('rating', '')):
		if( re.search('^[0-9](\.[0-9]*)?$', request.args.get('rating', ''))):
			foundMovies = []
			for movie in movies:
				if ( re.search('^[0-9](\.[0-9]*)?$', movie['Rating'])):
					if (float(movie['Rating']) > float(request.args.get('rating', ''))):
						foundMovies.append(movie)
			return jsonify(foundMovies), 200
		else:
			return jsonify({'Error':'Rating has to be between 0-10'}), 404
	else:
		return jsonify(movies), 200

@app.route('/movies/<movieID>', methods=['GET'])
def getMovieByID(movieID):
	if( request.args.get('embedded', '') == "album"):
		moviesEmb=copy.deepcopy(movies)
		r = requests.get('http://web1:81/albums/'+moviesEmb[int(movieID)]['Album_ID'])
		r = json.loads(r.text)
		moviesEmb[int(movieID)]['Album'] = r[0]
		return jsonify(moviesEmb[int(movieID)]), 200
	else:
		movieByID = [ movie for movie in movies if ( movie['ID'] == movieID)]
		return jsonify(movieByID), 200

@app.route('/movies', methods=['POST'])
def newMovie():
		if('Album' in request.json):
			album = request.json['Album']
			r = requests.post('http://web1:81/albums', json = {"Album" : album['Album'], "Artist" : album['Artist'], "Genre" : album['Genre'], "Producer" : album['Producer']})
			r = json.loads(r.text)
			numberOfMovies = len(movies)
			new_Movie={
						'ID' : str(numberOfMovies),
						'Title' : request.json['Title'],
						'Release_date' : request.json['Release_date'],
						'Rating' : request.json['Rating'],
						'Genre' : request.json['Genre'],
						'Album_ID' : r['ID']
						}
			movies.append(new_Movie)
			return jsonify(new_Movie), 201
		else:
			numberOfMovies = len(movies)
			r = requests.get('http://web1:81/albums/'+request.json['Album_ID'])
			if r.status_code == 404:
				return jsonify({'Error' : 'Album not found.'}), 404
			else:
				new_Movie={
						'ID' : str(numberOfMovies),
						'Title' : request.json['Title'],
						'Release_date' : request.json['Release_date'],
						'Rating' : request.json['Rating'],
						'Genre' : request.json['Genre'],
						'Album_ID' : request.json['Album_ID']
				}
				movies.append(new_Movie)
				return jsonify(new_Movie), 201

@app.route('/movies/<movieId>', methods=['PATCH'])
def rateMovie( movieId ):
		if( 'Album' in request.json ):
			r = requests.put('http://web1:81/albums/'+movies[int(movieId)]["Album_ID"], json = {"Album" : request.json['Album']['Album'], "Artist" : request.json['Album']['Artist'], "Genre" : request.json['Album']['Genre of Album'], "Producer" : request.json['Album']['Producer']})
			r = json.loads(r.text)[0]
			return jsonify(r), 200
		elif('Album_ID' in request.json):
			r = requests.get('http://web1:81/albums/'+request.json['Album_ID'])
			if r.status_code == 404:
				return jsonify({'Error' : 'Album not found.'}), 404
			else:
				movies[int(movieId)]["Album_ID"] = request.json['Album_ID']
				return jsonify(movies[int(movieId)]), 200
		else:
			rated = [ movie for movie in movies if ( movie['ID'] == movieId)]
			setRating = request.json['Rating']
			if(setRating == 10) or (re.search('^[0-9](\.[0-9]*)?$', setRating)):
				if (movies[int(movieId)]["Rating"] == "Not Rated"):
					movies[int(movieId)]["Rating"] = setRating
				else:
					rating = movies[int(movieId)]["Rating"]
					movies[int(movieId)]["Rating"] = (float(0 if rating == "Not Rated" else rating) + (0 if setRating == "Not Rated" else float(setRating))) / 2
				return jsonify(movies[int(movieId)]), 200
			else:
				return jsonify({'Error':'Rating has to be between 0-10'}), 404
#curl -i -X PUT -H "Content-Type: application/json" -d '{"Title": "Venom", "Release_date": "2018", "Rating": "Not Rated", "Genre": "Horror", "Album_ID": "2"}' localhost/movies/2
#curl -i -X PUT -H "Content-Type: application/json" -d '{"Title": "Venom", "Release_date": "2018", "Rating": "Not Rated", "Genre": "Horror", "Album": {"Album" : "1", "Artist" : "Mikutavicius", "Genre of Album" : "yra", "Producer" : "Mikutavicius"}}' localhost/movies/2
@app.route('/movies/<movieId>', methods=['PUT'])
def changeMovie( movieId ):
	if('Album' in request.json):
		movies[int(movieId)]['Title'] = request.json['Title']
		movies[int(movieId)]['Genre'] = request.json['Genre']
		movies[int(movieId)]['Rating'] = request.json['Rating']
		movies[int(movieId)]['Release_date'] = request.json['Release_date']
		r = requests.put('http://web1:81/albums/'+movies[int(movieId)]["Album_ID"], json = {"Album" : request.json['Album']['Album'], "Artist" : request.json['Album']['Artist'], "Genre" : request.json['Album']['Genre of Album'], "Producer" : request.json['Album']['Producer']})
		movies[int(movieId)]['Album'] = json.loads(r.text)[0]
		return jsonify(movies[int(movieId)]), 200
	else:
		r = requests.get('http://web1:81/albums/'+request.json['Album_ID'])
		if r.status_code == 404:
			return jsonify({'Error' : 'Album not found.'}), 404
		else:
			movies[int(movieId)]['Title'] = request.json['Title']
			movies[int(movieId)]['Genre'] = request.json['Genre']
			movies[int(movieId)]['Rating'] = request.json['Rating']
			movies[int(movieId)]['Release_date'] = request.json['Release_date']
			movies[int(movieId)]['Album_ID'] = request.json['Album_ID']
			return jsonify(movies[int(movieId)]), 200
#Deletes movie by ID curl -i -X DELETE localhost/movies/3
@app.route('/movies/<movieId>', methods=['DELETE'])
def removeMovie( movieId ):
        deleted = [ movie for movie in movies if ( movie['ID'] == movieId)]
        if len(deleted) == 0:
                return jsonify({'Delete failed' : 'ID not found.'}), 404
        else:
                movies.remove(deleted[0])
                return jsonify(deleted[0]), 200

if __name__ == "__main__":
        app.run(host="0.0.0.0", debug=True, port=5000)
