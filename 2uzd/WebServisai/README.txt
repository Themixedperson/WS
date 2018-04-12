List of albums

Running:
docker-compose up -d

Terminal query examples:
1. GET the list of albums: curl -i http://193.219.91.104:4355/albums
2. GET the album by the album ID: curl -i http://193.219.91.104:4355/albums/1
3. GET the list of albums by genre: curl -i http://193.219.91.104:4355/albums/genre/Jazz
4. POST (add) a new album: 
curl -i -X POST -H "Content-Type: application/json" -d '{ "ID": "3", "Album": "Prelude", 
<<<<<<< HEAD
"Artist": "April", "Genre": "Pop", "Producer": " "}' http://193.219.91.104:4355/albums/
=======
"Artist": "April", "Genre": "POP", "Producer": " "}' http://193.219.91.104:4355/albums
>>>>>>> 7748c8d120311263014bd059ad12ec67f4a66961
5. PUT (CHANGE) information about an album: 
curl -i -H "Content-type: application/json" -X PUT -d '{"Genre": "Pop"}' http://193.219.91.104:4355/albums/1
6. DELETE an album: curl -i -X DELETE http://193.219.91.104:4355/albums/1
