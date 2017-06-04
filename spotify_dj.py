import csv
import classes
from classes import *
from decimal import Decimal
from itertools import izip

scaleFactor = 10
requiredSim = .990
sugg_limit = 5
tracksPerList = 5
sp = classes.Spotify()

def get_field(field_name, list_values):
   return float(list_values[list_values.index(field_name) + 1])

def extract_feat_dict(csv_entry, features):
   list_values = csv_entry.split(",")
   feature_dict = {}

   name = list_values[0]

   for feature in features:
      feature_dict[feature] = get_field(feature, list_values)

   return name, feature_dict

def build_playlist(playlist_name, top_features):
   #user = Playlist("Pop Rising", sp, {"danceability": 0.6693300000000002, "acousticness": 0.13855849999999992, "energy": 0.6927300000000003, "liveness": 0.17840999999999993, "valence": 0.495797})
   #playlist_name = raw_input('Enter a playlist: ')
   user = Playlist(playlist_name, sp, dict.fromkeys(top_features))
   user.pull_features()

   return user

def build_sugg_playlists(database_file, top_features):
   playlists = []

   with open(database_file, 'rb') as csvFile:
      for row in csvFile:
         name, features = extract_feat_dict(row, top_features)
         curr_playlist = Playlist(name, sp, features)

         playlists.append(curr_playlist)

      return playlists

def suggest_songs(user, playlist, required_sim, sugg_limit, weight):
   songs_matched = 0

   playlist_user, playlist_id = sp.search_playlist(playlist.name)
   track_ids, track_names = sp.get_playlist_tracks(playlist_user, playlist_id)
   track_features = sp.get_features(track_ids)

   for track_name, track_feature in izip(track_names, track_features):
      track_sub_features = get_sub_dict(user.get_feature_keys(), track_feature)
      curr_track = Song(track_sub_features)

      sim = Profile.compare(user, curr_track, weight)

      if  sim >= required_sim:
         songs_matched += 1
         print "   ", track_name, " ", sim

      if songs_matched >= sugg_limit:
         break

def spotify_dj():#playlist_name, top_features, weight):
   # Features user are interested in
   top_features = ["danceability", "acousticness", "energy", "liveness", "valence"]
   weight = [5, 6, 3, 7, 7]
   playlist_name = "Rap Caviar"
   user = build_playlist(playlist_name, top_features)
   print user

   playlists = build_sugg_playlists('data.csv', top_features)

   for playlist in playlists:
      similarity = Profile.compare(user, playlist, weight)

      if similarity > requiredSim:
         print playlist.name, similarity

         suggest_songs(user, playlist, requiredSim, sugg_limit, weight)

if __name__ == '__main__':
   spotify_dj()
