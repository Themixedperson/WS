from flask import Flask
from redis import Redis
from flask import jsonify
from flask import request
import re
import os
app = Flask(__name__)
redis = Redis(host='redis', port=6379)
movies = [ {
			'ID' : '0',
			'Title' : 'Avengers: Infinity War',
			'Release date' : '05-2018',
			'Rating' : '5.3',
			'Genre' : 'Fantasy'
		   },
		   {
			'ID' : '1',
			'Title' : 'Avengers: Infinity War',
			'Release date' : '05-2018',
			'Rating' : 'Not Rated',
			'Genre' : 'Fantasy'
		   },
		   {
			'ID' : '2',
			'Title' : 'Avengers: Infinity War',
			'Release date' : '05-2018',
			'Rating' : '8.0',
			'Genre' : 'Fantasy'
		   },
	           {
			'ID' : '3',
			'Title' : 'Avengers: Infinity War',
			'Release date' : '05-2018',
			'Rating' : '3.75',
			'Genre' : 'Fantasy'
                   },
		   {
			'ID' : '4',
			'Title' : 'Avengers: Infinity War',
			'Release date' : '05-2018',
			'Rating' : 'Not Rated',
			'Genre' : 'Fantasy'
		   },
	 	   {
			'ID' : '5',
			'Title' : 'Avengers: Infinity War',
			'Release date' : '05-2018',
			'Rating' : 'Not Rated',
			'Genre' : 'Fantasy'
		   },
	 	   {
			'ID' : '6',
			'Title' : 'Alpha',
			'Release date' : '09-2018',
			'Rating' : 'Not Rated',
			'Genre' : 'Fantasy'
		   },
		   {
			'ID' : '7',
			'Title' : 'Fantastic Beasts: Crimes of Grundelvald',
			'Release date' : '11-2018',
			'Rating' : 'Not Rated',
			'Genre' : 'Fantasy'
		   },
		   {
			'ID' : '8',
			'Title' : 'Insidious: the last key',
			'Release date' : '01-2018',
			'Rating' : 'Not Rated',
			'Genre' : 'Horror'
		  }]

#Displays all movies
@app.route('/')
def hello():
	return jsonify({'All Movies':movies})

#Gets movies by title or part of it
#curl -i localhost/getMovieTitle/cr
@app.route('/getMovieTitle/<title>', methods=['GET'])
def getMovieTitle(title):
	foundMovies = []
	for i in movies:
		if( re.search(title, i["Title"], re.IGNORECASE)):
			foundMovies.append(i)
	return jsonify({'Results':foundMovies})

#Gets movies by genre
#curl -i localhost/getMovieGenre/Fantasy
@app.route('/getMovieGenre/<genre>', methods=['GET'])
def getMovieGenre(genre):
	foundMovies = [ movie for movie in movies if (movie['Genre'] == genre)]
	return jsonify({'Results':foundMovies})

#Gets movies with raiting equal or higher
#curl -i localhost/getMovieRating/2.5
@app.route('/getMovieRating/<rating>', methods=['GET'])
def getMovieRating(rating):
	if( re.search('^[0-9](\.[0-9]*)?$', rating)):
		foundMovies = []
        	for movie in movies:
			if ( re.search('^[0-9](\.[0-9]*)?$', movie['Rating'])):
				if (float(movie['Rating']) > float(rating)):
					  foundMovies.append(movie)
        	return jsonify({'Results':foundMovies})
	else:
		return jsonify({'Error':'Rating has to be between 0-10'})

#Creates new movie
#curl -i -X POST -H "Content-Type: application/json" -d '{"Title": "Venom", "Release date": "2018", "Rating": "Not Rated", "Genre": "Horror"}'
#localhost/newMovie
@app.route('/newMovie', methods=['POST'])
def newMovie():
	numberOfMovies = len(movies)
	new_Movie={
		'ID' : numberOfMovies,
		'Title' : request.json['Title'],
		'Release date' : request.json['Release date'],
		'Rating' : request.json['Rating'],
		'Genre' : request.json['Genre']
	}
	movies.append(new_Movie)
	return jsonify({'Added': new_Movie})

#Rate movie
#Rating is calculated automatically
#curl -i -X PUT -H "Content-Type: application/json" -d '{"Rating": "5"}' localhost/rateMovie/2
@app.route('/rateMovie/<movieId>', methods=['PUT'])
def rateMovie( movieId ):
        rated = [ movie for movie in movies if ( movie['ID'] == movieId)]
        setRating = request.json['Rating']
	if(setRating == 10) or (re.search('^[0-9](\.[0-9]*)?$', setRating)):
		if (movies[int(movieId)]["Rating"] == "Not Rated"):
                	movies[int(movieId)]["Rating"] = setRating
        	else:
                	rating = movies[int(movieId)]["Rating"]
                	movies[int(movieId)]["Rating"] = (float(0 if rating == "Not Rated" else rating) + (0 if setRating == "Not Rated" else float(setRating))) / 2
        	return jsonify({'Rated Movie':movies[int(movieId)]})
	else:
		return jsonify({'Error':'Rating has to be between 0-10'})

#Deletes movie by ID
#curl -i -X DELETE localhost/deleteMovie/3
@app.route('/removeMovie/<movieId>', methods=['DELETE'])
def removeMovie( movieId ):
	deleted = [ movie for movie in movies if ( movie['ID'] == movieId)]
	if len(deleted) == 0:
		return jsonify({'Delete failed' : 'ID not found.'})
	else:
		movies.remove(deleted[0])
		return jsonify({'Removed Movie':deleted[0]})

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
