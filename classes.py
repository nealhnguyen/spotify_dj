import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class Song:
   def __init__(self, profile):
      self.profile = profile

class Playlist:
   def __init__(self, profile):
      self.profile = profile

class Profile:
   'Common profile class for all playlists'
   def __init__(self, features={}):
      self.features = features

   def __repr__(self):
      profile_repr = ""

      features = self.features
      for feature in features:
         profile_repr += feature + " " + str(features[feature]) + "\n"

      return profile_repr

   def edit_feature(self, feature, val):
      self.features[feature] = val

   def get_features(self):
      allKeys = self.features.keys()
      for key in allKeys:
         print(key)
      print('\n')

   #def __init__(self, feat1, val1, feat2, val2, feat3, val3, feat4, val4, feat5, val5):
   #   self.features = {}
   #   self.features[feat1] = val1
   #   self.features[feat2] = val2
   #   self.features[feat3] = val3
   #   self.features[feat4] = val4
   #   self.features[feat5] = val5
   #def edit(self, feat1, val1, feat2, val2, feat3, val3, feat4, val4, feat5, val5):
   #   self.features[feat1] = val1
   #   self.features[feat2] = val2
   #   self.features[feat3] = val3
   #   self.features[feat4] = val4
   #   self.features[feat5] = val5

  # def getTopFeatures(self):
  #    allKeys = self.features.keys()
  #    for key in allKeys:
  #       print(key)
  #    print('\n')
#
  # def getDetailedFeatures(self):
  #    details = self.features.items()
  #    for item in details:
  #       print(item)
  #    print('\n')

class Spotify:
   GET_ARTIST_ENDPOINT = 'https://api.spotify.com/v1/artists/{id}'
   SEARCH_ENDPOINT = 'https://api.spotify.com/v1/search'
   RELATED_ARTISTS_ENDPOINT = 'https://api.spotify.com/v1/artists/{id}/related-artists'
   TOP_TRACKS_ENDPOINT = 'https://api.spotify.com/v1/artists/{id}/top-tracks'
   AUDIO_FEATURE = 'https://api.spotify.com/v1/audio-features/{id}'

   client_credentials_manager = SpotifyClientCredentials(client_id = 'a64e7ced0f1d40c0960a9f13608c4e37', client_secret = '139896904200432696a1ffda522daa7e')
   sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
   sp.trace=False

   def get_artist(artist_id):
      url = GET_ARTIST_ENDPOINT.format(id=artist_id)
      resp = requests.get(url)
      return resp.json()

   def search_by_artist_name(name):
      myparams = {'type': 'artist'}
      myparams['q'] = name
      resp = requests.get(SEARCH_ENDPOINT, params=myparams)
      return resp.json()

   def get_related_artists(artist_id):
      url = RELATED_ARTISTS_ENDPOINT.format(id=artist_id)
      resp = requests.get(url)
      return resp.json()

   def get_artist_top_tracks(artist_id, country='US'):
      url = TOP_TRACKS_ENDPOINT.format(id=artist_id)
      myparams = {'country': country}
      resp = requests.get(url, params=myparams)
      return resp.json()

   def get_audio_features(track_id, country='US'):
      url = AUDIO_FEATURE.format(id=track_id)
      resp = requests.get(AUDIO_FEATURE)
      return resp.json()

   def get_track_features(self, trackID):
      sp = self.sp
      features = sp.audio_features(trackID)
      return (features)

   def get_playlist_tracks(self, playlistName):
      sp = self.sp
      track_list = []
      results = sp.search(q=playlistName, type='playlist')
      check = results['playlists']['total']
      if check == 0 :
         return -1
      else :
         uri = results['playlists']['items'][0]['uri']
         username = uri.split(':')[2]
         playlist_id = uri.split(':')[4]
         results = sp.user_playlist(username, playlist_id)
         for song in results['tracks']['items']:
            #print song['track']['id']
            #print(song['track']['name'])
            if not (song['track']['name'] is None and song['track']['id'] is None):
               # List of tuple (name, id)
               track_list.append((song['track']['name'], song['track']['id'].encode('utf-8')))

         return track_list
