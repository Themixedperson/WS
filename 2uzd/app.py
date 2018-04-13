from flask import Flask
from redis import Redis
from flask import jsonify
from flask import request
import requests
import json
app = Flask(__name__)
movies = [ {
                        'ID' : '0',
                        'Title' : 'Avengers: Infinity War',
                        'Release date' : '05-2018',
                        'Rating' : '5.3',
                        'Genre' : 'Fantasy',
			'Album ID' : '1'
                   },
                   {
                        'ID' : '1',
                        'Title' : 'Avengers: Infinity War',
                        'Release date' : '05-2018',
                        'Rating' : 'Not Rated',
                        'Genre' : 'Fantasy',
			'Album ID' : '1'
                   },
                   {
                        'ID' : '2',
                        'Title' : 'Movie_1',
                        'Release date' : '05-2018',
                        'Rating' : '8.0',
                        'Genre' : 'Fantasy',
			'Album ID' : '1'
                   },
                   {
                        'ID' : '3',
                        'Title' : 'Movie_2',
                        'Release date' : '05-2018',
                        'Rating' : '3.75',
                        'Genre' : 'Fantasy',
			'Album ID' : '1'
                   },
                   {
                        'ID' : '4',
                        'Title' : 'Movie_3',
                        'Release date' : '05-2018',
                        'Rating' : 'Not Rated',
                        'Genre' : 'Fantasy',
			'Album ID' : '1'
                   },
                   {
                        'ID' : '5',
                        'Title' : 'Avengers: Infinity War',
                        'Release date' : '05-2018',
                        'Rating' : 'Not Rated',
                        'Genre' : 'Fantasy',
			'Album ID' : '1'
                   },
                   {
                        'ID' : '6',
                        'Title' : 'Alpha',
                        'Release date' : '09-2018',
                        'Rating' : 'Not Rated',
                        'Genre' : 'Fantasy',
			'Album ID' : '1'
                   },
                   {
                        'ID' : '7',
                        'Title' : 'Fantastic Beasts: Crimes of Grundelvald',
                        'Release date' : '11-2018',
                        'Rating' : 'Not Rated',
                        'Genre' : 'Fantasy',
			'Album ID' : '1'
                   },
                   {
                        'ID' : '8',
                        'Title' : 'Insidious: the last key',
                        'Release date' : '01-2018',
                        'Rating' : 'Not Rated',
                        'Genre' : 'Horror',
			'Album ID' : '10'
                  }]
#Displays all movies
#curl -i localhost curl -i localhost/movies?title=<title> curl -i localhost/movies?genre=<genre> Gets movies with raiting equal or higher curl -i localhost/getMovieRating/2.5
@app.route('/movies', methods=['GET'])
def hello():
	if( request.args.get('title', '')):
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
	movieByID = [ movie for movie in movies if ( movie['ID'] == movieID)]
	return jsonify(movieByID), 200

#Creates new movie
#curl -i -X POST -H "Content-Type: application/json" -d '{"Title": "Venom", "Release date": "2018", "Rating": "Not Rated", "Genre": "Horror", "Album ID" : "1"}' localhost/newMovie
@app.route('/movies', methods=['POST'])
def newMovie():
		numberOfMovies = len(movies)
		r = requests.get('http://172.18.0.1:81/albums/'+request.json['Album ID'])
		if r.status_code == 404:
			return jsonify({'Error' : 'Album not found.'}), 404
		else:
			new_Movie={
					'ID' : numberOfMovies,
					'Title' : request.json['Title'],
					'Release date' : request.json['Release date'],
					'Rating' : request.json['Rating'],
					'Genre' : request.json['Genre'],
					'Album ID' : request.json['Album ID']
			}
			movies.append(new_Movie)
			return jsonify(new_Movie), 201

#Rate movie
#curl -i -X PATCH -H "Content-Type: application/json" -d '{"Rating": "5"}' localhost/movies/rated/2
@app.route('/movies/<movieId>', methods=['PATCH'])
def rateMovie( movieId ):
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

#curl -i -X PUT -H "Content-Type: application/json" -d '{"Title": "Venom", "Release date": "2018", "Rating": "Not Rated", "Genre": "Horror"}' localhost/movies/updated/2
@app.route('/movies/<movieId>', methods=['PUT'])
def changeMovie( movieId ):
	changed = [ movie for movie in movies if ( movie['ID'] == movieId)]
	movies[int(movieId)]['Title'] = request.json['Title']
	movies[int(movieId)]['Genre'] = request.json['Genre']
	movies[int(movieId)]['Rating'] = request.json['Rating']
	movies[int(movieId)]['Release date'] = request.json['Release date']
	return jsonify(movies[int(movieId)]), 200

#Deletes movie by ID
#curl -i -X DELETE localhost/movies/3
@app.route('/movies/<movieId>', methods=['DELETE'])
def removeMovie( movieId ):
        deleted = [ movie for movie in movies if ( movie['ID'] == movieId)]
        if len(deleted) == 0:
                return jsonify({'Delete failed' : 'ID not found.'}), 404
        else:
                movies.remove(deleted[0])
                return jsonify(deleted[0]), 200

#Get Album by movie ID
#curl -i localhost/movie/<movieID>/album
@app.route('/movies/<movieId>/album', methods=['GET'])
def getAlbum(movieId):
	r = requests.get('http://web1:81/albums/'+movies[int(movieId)]['Album ID'])
	if r.status_code == 404:
		return jsonify({'Error' : 'Album not found.'}), 404
	else:
		r = json.loads(r.text)
		return jsonify(r), 200

#Creates new movie and new album
#curl -i -X POST -H "Content-Type: application/json" -d '{"Title": "Venom", "Release date": "2018", "Rating": "Not Rated", "Genre": "Horror", "Album" : "1", "Artist" : "Mikutavicius", "Genre of Album" : "yra", "Producer" : "Mikutavicius"}' localhost/movies/album
@app.route('/movies/album', methods=['POST'])
def newMovieAlbum():
	r = requests.post('http://web1:81/albums', json = {"Album" : request.json['Album'], "Artist" : request.json['Artist'], "Genre" : request.json['Genre of Album'], "Producer" : request.json['Producer']})
	r = json.loads(r.text)
	numberOfMovies = len(movies)
	new_Movie={
				'ID' : numberOfMovies,
				'Title' : request.json['Title'],
				'Release date' : request.json['Release date'],
				'Rating' : request.json['Rating'],
				'Genre' : request.json['Genre'],
				'Album ID' : r['ID']
				}
	movies.append(new_Movie)
	return jsonify(new_Movie), 201

#curl -i -X PUT -H "Content-Type: application/json" -d '{"Album" : "1", "Artist" : "Mikutavicius", "Genre of Album" : "yra", "Producer" : "Mikutavicius"}' localhost/movies/<movieID>/album
@app.route('/movies/<movieId>/album', methods=['PUT'])
def changeMovieAlbum( movieId ):
	r = requests.put('http://web1:81/albums/'+movies[int(movieId)]["Album ID"], json = {"Album" : request.json['Album'], "Artist" : request.json['Artist'], "Genre" : request.json['Genre of Album'], "Producer" : request.json['Producer']})
	r = json.loads(r.text)
	return jsonify(r), 200

#Changes movie AlbumID
#curl -i -X PATCH -H "Content-Type: application/json" -d '{"Album ID": "2"}' localhost/movies/2/album
@app.route('/movies/<movieId>/album', methods=['PATCH'])
def changeAlbum(movieId):
	r = requests.get('http://web1:81/albums/'+request.json['Album ID'])
	if r.status_code == 404:
		return jsonify({'Error' : 'Album not found.'}), 404
	else:
		movies[int(movieId)]["Album ID"] = request.json['Album ID']
		return jsonify(movies[int(movieId)]), 200

if __name__ == "__main__":
        app.run(host="0.0.0.0", debug=True, port=5000)
