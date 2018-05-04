#Build and run
docker-compose build
docker-compose up -d
-----------------NEW FUNCTIONALITY-------------
#Displays movie and album
curl -i localhost/movies/<movieID>?embedded=album

#Creates new movie and new album
curl -i -X POST -H "Content-Type: application/json" -d '{"Title": "Venom", "Release_date": "2018", "Rating": "Not Rated", "Genre": "Horror", "Album" : {"Album" : "1", "Artist" : "Mikutavicius", "Genre of Album" : "yra", "Producer" : "Mikutavicius"}}' localhost/movies?embedded=album

#Changes movie and album
curl -i -X PUT -H "Content-Type: application/json" -d '{"Album" : "1", "Artist" : "Mikutavicius", "Genre of Album" : "yra", "Producer" : "Mikutavicius"}' localhost/movies/<movieID>

#Changes movie AlbumID if it exists
curl -i -X PATCH -H "Content-Type: application/json" -d '{"Album_ID": "2"}' localhost/movies/<movie_id>
-----------------------------------------------
#Displays all movies
curl -i localhost

#Search title
curl -i localhost/movies?title=<title>

#Search genre
curl -i localhost/movies?genre=<genre>

#Search rating equal or higher
curl -i localhost/movies?raiting=<raiting>

#Creates new movie
curl -i -X POST -H "Content-Type: application/json" -d '{"Title": "Venom", "Release_date": "2018", "Rating": "Not Rated", "Genre": "Horror", "Album_ID" : "1"}' localhost/movies

#Rate movie (update raiting)
curl -i -X PATCH -H "Content-Type: application/json" -d '{"Rating": "5"}' localhost/movies/<movie_id>

#Update move
curl -i -X PUT -H "Content-Type: application/json" -d '{"Title": "Venom", "Release date": "2018", "Rating": "Not Rated", "Genre": "Horror"}' 193.219.91.103:4496/moviess/<ID>

#Deletes movie by ID
curl -i -X DELETE localhost/movies/<movie_id>
