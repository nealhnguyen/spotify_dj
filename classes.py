import requests
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def avg_dicionaries(dict_list):
   for key_dict in dict_list:
      for key, val in key_dict.iteritems():
         avg[key] += float(val)

   return {key: value / len(data) for key, value in avg.iteritems()}

def get_sub_dict(keys, the_dict):
   sub_dict = {}

   for key in keys:
      sub_dict[key] = the_dict[key]

   return sub_dict

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

class Song(Profile):
   def __init(self, name, features={}):
      self.name = name
      super.__init__(Song,features)

class Playlist(Profile):
   def __init__(self, name, sp, feature_keys=[]):
      self.name = name
      self.sp = sp

      features = make_features(name, feature_keys)
      super.__init__(Playlist, features)

   #make the features for a playlist profile by averaging all the track features
   def make_features(self, name, feature_keys):
      if not feature_keys:
         return []

      sp = self.sp

      username, playlist_id = sp.search_playlist(name)
      tracks = sp.get_playlist_tracks(username, playlist_id)

      tracks_features = sp.get_track_features(track)

      features = avg_dicionaries(tracks_features)

      return get_sub_dict(feature_keys, features)

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

   def get_features(self, track_id):
      features = self.sp.audio_features(track_id)

      return features

   def search_playlist(self, playlist_name):
      track_list = []
      results = self.sp.search(q=playlist_name, type='playlist')
      check = results['playlists']['total']

      if check == 0 :
         print "invalid search"
         sys.exit()

      uri = results['playlists']['items'][0]['uri']

      username = uri.split(':')[2]
      playlist_id = uri.split(':')[4]

      return username, playlist_id

   def get_playlist_tracks(self, username, playlist_id):
      results = self.sp.user_playlist(username, playlist_id)
      track_ids = []
      track_names = []
      for track in results['tracks']['items']:
         track_ids.append(track['track']['uri'])
         track_names.append(track['track']['name'])

      return track_ids, track_names
