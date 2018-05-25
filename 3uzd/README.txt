#Build and run
sudo docker-compose up -d

########REST#######
#Displays all movies
curl -i localhost/movies
#Search title
curl -i localhost/movies?title=<title>
#Search genre
curl -i localhost/movies?genre=<genre>
#Search rating equal or higher
curl -i localhost/movies?rating=<rating>
#Creates new movie
curl -i -X POST -H "Content-Type: application/json" -d '{"Title": "Venom", "Release date": "2018", "Rating": "Not Rated", "Genre": "Horror"}' localhost/movies
#Update rating
curl -i -X PATCH -H "Content-Type: application/json" -d '{"Rating": "5"}' localhost/movies/<ID>
#Update move
curl -i -X PUT -H "Content-Type: application/json" -d '{"Title": "Venom", "Release date": "2018", "Rating": "Not Rated", "Genre": "Horror"}' localhost/movies/<ID>
#Deletes movie by ID
curl -i -X DELETE localhost/movies/<ID>

#######SOUP######
python req.py

