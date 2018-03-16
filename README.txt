
#Build and run
sudo docker-compose up -d
#Main page (list all movies) curl -i 193.219.91.103:1994 Search Movie by 
#title curl -i 193.219.91.103:1994/getMovieTitle/<search word> Search movies 
#by genre curl -i 193.219.91.103:1994/getMovieGenre/<genre> Search movies 
#with raiting equal or higher curl -i 
#193.219.91.103:1994/getMovieRating/<numeric rating> Create new movie curl -i 
#-X POST -H "Content-Type: application/json" -d '{"Title": "<title>", 
#"Release date": "<date>", "Rating": "<rating>", "Genre": "<genre>"}' 
#193.219.91.103:1994/newMovie Rate movie Rating is calculated automatically 
#curl -i -X PUT -H "Content-Type: application/json" -d '{"Rating": "<rating>"}' 
#193.219.91.103:1994/rateMovie/<rating> Deletes movie by ID
#curl -i -X DELETE 193.219.91.103:1994/deleteMovie/<ID>
