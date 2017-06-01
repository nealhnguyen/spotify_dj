import json
import csv
import classes
from classes import Profile
from classes import Song
from classes import Playlist
from decimal import Decimal
from sim import cos_sim

scaleFactor = 10
reqPlaylistSim = .995
reqTrackSim = .990
tracksPerList = 5
sp = classes.Spotify()

#make a profile given a specific playlist name and the features that we want to use
def makeProfile(playlistName, feat1, feat2, feat3, feat4, feat5):
    value1 = 0
    value2 = 0
    value3 = 0
    value4 = 0
    value5 = 0
    value6 = 0

    track_list = []

    track_list = sp.get_playlist_tracks(playlistName)
    for (name, trackId) in track_list:
       features = get_track_features(trackId)
       for feature in features:
         value1 += feature[feat1]
         value2 += feature[feat2]
         value3 += feature[feat3]
         value4 += feature[feat4]
         value5 += feature[feat5]

    avg1 = value1/len(track_list)
    avg2 = value2/len(track_list)
    avg3 = value3/len(track_list)
    avg4 = value4/len(track_list)
    avg5 = value5/len(track_list)

    profile = Profile(feat1, avg1, feat2, avg2, feat3, avg3, feat4, avg4, feat5, avg5)
    return profile

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
   playList = "Pop Rising"
   profile = Profile({"danceability": 0.6693300000000002, "acousticness": 0.13855849999999992, "energy": 0.6927300000000003, "liveness": 0.17840999999999993, "valence": 0.495797})

   with open('data.csv', 'rb') as csvFile:
      for row in csvFile:
         listValues = row.split(",")

         name = listValues[0]
         acousticness = get_field("acousticness", listValues)
         danceability = get_field("danceability", listValues)
         energy = get_field("energy", listValues)
         liveness = get_field("liveness", listValues)
         valence = get_field("valence", listValues)

         if name != playList:
            tempProfile = Profile({"danceability": danceability, "acousticness": acousticness, "energy": energy, "liveness": liveness, "valence": valence})
            similarity = compareProfile(profile, tempProfile)
         else:
            similarity = 0

         print "Name: ", name, " Similarity: ", similarity

         if similarity >= reqPlaylistSim:
            count = 0
            tracks = sp.get_playlist_tracks(name)
            for name, trackId in tracks:
               features = sp.get_track_features(trackId)
               for feature in features:
                  danceability = feature["danceability"]
                  acousticness = feature["acousticness"]
                  energy = feature["energy"]
                  liveness = feature["liveness"]
                  valence = feature["valence"]

               tempProfile = Profile({"danceability": danceability, "acousticness": acousticness, "energy": energy, "liveness": liveness, "valence": valence})
               sim = compareProfile(profile, tempProfile)

               if  sim >= reqTrackSim:
                  count += 1
                  print name, " ", sim

               if count >= 5:
                  print "\n"
                  break

if __name__ == '__main__':
   main()