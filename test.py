from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import spotify
import json

results = spotify.search_by_artist_name('kanye west')
artists = results['artists']
artists = artists['items']

artistId = artists[0]['id']
relatedArtists = spotify.get_related_artists(artistId)

client_credentials_manager = SpotifyClientCredentials(client_id = 'a64e7ced0f1d40c0960a9f13608c4e37', client_secret = '139896904200432696a1ffda522daa7e')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace=True

song_ids = []
for artist in relatedArtists['artists']:
   print artist['name']
   results = spotify.search_by_artist_name(artist['name'])
   artists = results['artists']
   artists = artists['items']
   artistId = artists[0]['id']

   topTracks = spotify.get_artist_top_tracks(artistId, country='US')

   for tracks in topTracks['tracks']:
     #print '\t' + tracks['name']
     #features = spotify.get_audio_features(tracks['id'], country='US')
     #features = sp.audio_features(tracks['id']
     trackID = tracks['id'].encode('utf-8')
     features = sp.audio_features(trackID)
