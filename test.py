import spotipy
import spotify

sp = spotipy.Spotify()

results = spotify.search_by_artist_name('kanye west')
artists = results['artists']
artists = artists['items']

artistId = artists[0]['id']
relatedArtists = spotify.get_related_artists(artistId)
   
for artist in relatedArtists['artists']:
   print artist['name']
   results = spotify.search_by_artist_name(artist['name'])
   artists = results['artists']
   artists = artists['items']
   artistId = artists[0]['id']

   topTracks = sp.artist_top_tracks(artistId, country='US')

   for tracks in topTracks['tracks']:
      print '\t' + tracks['name']

