from suds.client import Client as SudsClient

url = 'http://localhost/soap/movies?wsdl'
client = SudsClient(url=url, cache=None)
r = client.service.newMovieAlbumSoap("Title", "Genre", "Not Rated", "Not Released", "a", "b", "c", "d")
#r = client.service.rateMovieSoap("5","8")
#r = client.service.changeMovieSoap("1","Title", "Genre", "Not Rated", "Not Released", "1")
#r = client.service.deleteMovieSoap("1")
#r = client.service.getMoviesAlbumsSoap()
#r = client.service.changeMovieAlbumSoap("1","Title", "Genre", "Not Rated", "Not Released", "a", "a", "t", "y")
print r
print client.last_sent()
print client.last_received()
