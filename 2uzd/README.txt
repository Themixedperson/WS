#Build and run
docker-compose build
docker-compose up -d
-----------------NEW FUNCTIONALITY-------------
#Displays movie album
curl -i 193.219.91.103:4496/movies/<movieID>/album

#Creates new movie and album
curl -i -X POST -H "Content-Type: application/json" -d '{"Title": "Venom", "Release date": "2018", "Rating": "Not Rated", "Genre": "Horror", "Album" : "1", "Artist" : "Mikutavicius", "Genre of Album" : "yra", "Producer" : "Mikutavicius"}' 193.219.91.103:4496/movies/album

#Changes movie album info
curl -i -X PUT -H "Content-Type: application/json" -d '{"Album" : "1", "Artist" : "Mikutavicius", "Genre of Album" : "yra", "Producer" : "Mikutavicius"}' 193.219.91.103:4496//movies/<movieID>/album

#Changes movie ALbumID if it exists
#curl -i -X PATCH -H "Content-Type: application/json" -d '{"Album ID": "2"}' 193.219.91.103:4496/movies/<movieID>/album
-----------------------------------------------
#Displays all movies
curl -i 193.219.91.103:4496/movies

#Search title
curl -i 193.219.91.103:4496/movies?title=<title>

#Search genre
curl -i 193.219.91.103:4496/movies?genre=<genre>

#Search rating equal or higher
curl -i 193.219.91.103:4496/movies?rating=<rating>

#Creates new movie
curl -i -X POST -H "Content-Type: application/json" -d '{"Title": "Venom", "Release date": "2018", "Rating": "Not Rated", "Genre": "Horror"}' 193.219.91.103:4496/movies

#Update rating
curl -i -X PATCH -H "Content-Type: application/json" -d '{"Rating": "5"}' 193.219.91.103:4496/movies/<ID>

#Update move
curl -i -X PUT -H "Content-Type: application/json" -d '{"Title": "Venom", "Release date": "2018", "Rating": "Not Rated", "Genre": "Horror"}' 193.219.91.103:4496/moviess/<ID>

#Deletes movie by ID
curl -i -X DELETE 193.219.91.103:4496/movies/<ID>
