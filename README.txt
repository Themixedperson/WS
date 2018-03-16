#Build and run
sudo docker-compose up -d
#Displays all movies
curl -i localhost/movies
#Search title
curl -i localhost/movies?title=<title>
#Search genre
curl -i localhost/movies?genre=<genre>
#Search rating equal or higher
curl -i localhost/movies?rating=<rating>
#Creates new movie
curl -i -X POST -H "Content-Type: application/json" -d '{"Title": "Venom", "Release date": "2018", "Rating": "Not Rated", "Genre": "Horror"}' localhost/movies/new
#Update rating
curl -i -X PATCH -H "Content-Type: application/json" -d '{"Rating": "5"}' localhost/movies/rated/2
#Update move
curl -i -X PUT -H "Content-Type: application/json" -d '{"Title": "Venom", "Release date": "2018", "Rating": "Not Rated", "Genre": "Horror"}' localhost/updated/2
#Deletes movie by ID
curl -i -X DELETE localhost/movies/deleted/3
