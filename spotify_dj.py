import json
import csv
import classes
from classes import Profile
from classes import Song
from classes import Playlist
from decimal import Decimal
from itertools import izip
from sim import cos_sim

scaleFactor = 10
requiredSim = .995
tracksPerList = 5
sp = classes.Spotify()


#comparing the profiles of the two playlists
def compareProfile(playlist1, playlist2):
   vector1 = []
   vector2 = []
   details = playlist1.features.items()

   for item in details:
      vector1.append(item[1] * scaleFactor)

   details = playlist2.features.items()
   for item in details:
      vector2.append(item[1] * scaleFactor)

   return cos_sim(vector1, vector2)

def get_field(field_name, list_values):
   return float(list_values[list_values.index(field_name) + 1])

def main():
#   playList = raw_input('Enter a playlist: ')
#   print playList
#   profile = makeProfile(playList, "danceability", "acousticness", "energy", "liveness", "tempo")
#   print profile

   # Pop Rising
   user_playlist = Playlist(name, sp, {"danceability": 0.6693300000000002, "acousticness": 0.13855849999999992, "energy": 0.6927300000000003, "liveness": 0.17840999999999993, "valence": 0.495797})
   print profile

   with open('data.csv', 'rb') as csvFile:
      for row in csvFile:
         listValues = row.split(",")

         name = listValues[0]
         acousticness = get_field("acousticness", listValues)
         danceability = get_field("danceability", listValues)
         energy = get_field("energy", listValues)
         liveness = get_field("liveness", listValues)
         valence = get_field("valence", listValues)

         tempProfile = Profile({"danceability": danceability, "acousticness": acousticness, "energy": energy, "liveness": liveness, "valence": valence})

         similarity = compareProfile(profile, tempProfile)

         if similarity >= requiredSim:
            print "Name: ", name, " Similarity: ", similarity
            count = 0

            username, playlist_id = sp.search_playlist(name)
            track_ids, track_names = sp.get_playlist_tracks(username, playlist_id)
            track_features = sp.get_features(track_ids)

            for track_name, track_feature in izip(track_names, track_features):
               tempProfile = Profile(track_feature)
               sim = compareProfile(profile, tempProfile)

               if  sim >= .990:
                  count += 1
                  print track_name, " ", sim

               if count >= 5:
                  break
      sys.exit()

if __name__ == '__main__':
   main()
