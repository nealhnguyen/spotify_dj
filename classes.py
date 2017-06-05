import requests
import json
import spotipy
from sim import cos_sim
from spotipy.oauth2 import SpotifyClientCredentials

def avg_dicts(dict_list, features_of_intrest):
   avg = dict.fromkeys(features_of_intrest, 0)

   for temp_dict in dict_list:
      curr_dict = get_sub_dict(features_of_intrest, temp_dict)
      for key, val in curr_dict.items():
         avg[key] += float(val)

   return {key: value / len(dict_list) for key, value in avg.iteritems()}

def get_sub_dict(keys, the_dict):
   sub_dict = {}

   for key in keys:
      sub_dict[key] = the_dict[key]

   return sub_dict

class Profile(object):
   'Common profile class for all playlists'
   def __init__(self, features={}):
      self.features = features

   def __repr__(self):
      return json.dumps(self.features, indent=3)[2:-2]

   def edit_feature(self, feature, val):
      self.features[feature] = val

   def print_features(self):
      allKeys = self.features.keys()
      for key in allKeys:
         print(key)
      print('\n')

   def get_feature_keys(self):
      return sorted(self.features.keys())

   #comparing the profiles of the two playlists
   def compare(profile1, profile2, weight):
      if not isinstance(profile1, Profile) or not isinstance(profile2, Profile):
         print "ERROR: profile1 and 2 are not both a <Profile> type"
         sys.exit()

      vector1 = []
      vector2 = []
      weight_list = []

      for key in profile1.get_feature_keys():
         # sometimes a feature doesn't have a value, ignore this song
         if profile2.features[key] is None:
            return 0

         vector1.append(profile1.features[key])
         vector2.append(profile2.features[key])
         weight_list.append(weight[key])

      return cos_sim(vector1, vector2, weight_list)

class Song(Profile):
   def __init(self, features={}):
      Profile.__init__(self, features)

   def __repr__(self):
      return self.name + "\n" + Profile.__repr__(self)

class Playlist(Profile):
   def __init__(self, name, sp, features={}):
      Profile.__init__(self, features)
      self.name = name
      self.sp = sp

   def __repr__(self):
      return self.name + "\n" + Profile.__repr__(self)

   #make the features for a playlist profile by averaging all the track features
   def pull_features(self):
      if not self.features:
         return

      feature_keys = self.features.keys()

      username, playlist_id = self.sp.search_playlist(self.name)
      track_ids, track_names = self.sp.get_playlist_tracks(username, playlist_id)

      tracks_features = self.sp.get_features(track_ids)

      self.features = avg_dicts(tracks_features, self.get_feature_keys())

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
