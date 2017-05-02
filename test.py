from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import spotify
import json

class Song:
    def __init__(self, profile):
        self.profile = profile

class Playlist:
    def __init__(self, profile):
        self.profile = profile

class Profile: 
    'Common profile class for all playlists'
    def __init__(self, variance, feat1, val1, feat2, val2, feat3, val3):
        self.features = {}
        self.features[feat1] = val1
        self.features[feat2] = val2
        self.features[feat3] = val3

        self.variance = variance

    def edit(self, variance, feat1, val1, feat2, val2, feat3, val3):
        self.variance = variance
        self.features[feat1] = val1
        self.features[feat2] = val2
        self.features[feat3] = val3

    def getTopFeatures(self):
        allKeys = self.features.keys()
        for key in allKeys:
            print(key)
        print('\n')

    def getDetailedFeatures(self):
        details = self.features.items()
        for item in details:
            print(item)
        print('\n')
    

results = spotify.search_by_artist_name('kanye west')
artists = results['artists']
artists = artists['items']

artistId = artists[0]['id']
relatedArtists = spotify.get_related_artists(artistId)

client_credentials_manager = SpotifyClientCredentials(client_id = 'a64e7ced0f1d40c0960a9f13608c4e37', client_secret = '139896904200432696a1ffda522daa7e')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace=False

profile1 = Profile(7, "tempo", 3.2, "melody", 1.0, "liveliness", 2.3)
profile1.getDetailedFeatures()

profile1.edit(7, "tempo", 1.2, "melody", 1.0, "liveliness", 2.3)
profile1.getDetailedFeatures()

song_ids = []
for artist in relatedArtists['artists']:
   #print(artist['name'])
'''for artist in relatedArtists['artists']:
   print artist['name']
   results = spotify.search_by_artist_name(artist['name'])
   artists = results['artists']
   artists = artists['items']
   artistId = artists[0]['id']

   topTracks = spotify.get_artist_top_tracks(artistId, country='US')

   for tracks in topTracks['tracks']:
     #print('\t' + tracks['name'])
     #features = spotify.get_audio_features(tracks['id'], country='US')
     #features = sp.audio_features(tracks['id'])
     trackID = tracks['id'].encode('utf-8')
     features = sp.audio_features(trackID)'''

def get_track_features(trackID):
   features = sp.audio_features(trackID)
   print features

def get_playlist_tracks(playlistName):
   results = sp.search(q=playlistName, type='playlist')
   uri = results['playlists']['items'][0]['uri']
   username = uri.split(':')[2]
   playlist_id = uri.split(':')[4]
   results = sp.user_playlist(username, playlist_id)
   for song in results['tracks']['items']:
       #print song['track']['id']
       print song['track']['name']
       if not (song['track']['id'] is None):
          track_list.append(song['track']['id'].encode('utf-8'))

track_list = []
playlistName = 'Daily Lift'
get_playlist_tracks(playlistName)
for track in track_list:
   get_track_features(track)
