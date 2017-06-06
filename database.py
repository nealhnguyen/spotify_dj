import csv
import classes
from classes import * 
from spotify_dj import build_playlist 

dataFile = "data3.csv"
sp = classes.Spotify()

def databaseUpdate():
   playlists = ["Hot Rhythmic", "Good Vibes", "RapCaviar", "Chill Hits", "electroNOW", "Hot Country", "Rock This", "Are & Be"]
   playlists += ["Pop Rising", "Have a Great Day!", "Most Necessary", "Pop Chillout", "dancePop", "New Boots", "New Noise", "The Newness", "Teen Party", "Morning Accoustic"]
   playlists += ["Get Turnt", "Signed XOXO", "Fresh & Chill", "Happy Chill Good Time Vibes", "Chill Vibes", "Beach Vibes", "Tropical House", "Dance Hits", "Country Gold", "Country Kind of Love"]

   for playlist in playlists:
      print playlist
      top_features = ["danceability", "acousticness", "energy", "liveness", "valence"]
      profile = build_playlist(playlist, top_features)
      dataList = []
      details = profile.features.items()

      dataList.append(playlist)

      username, playlist_id = sp.search_playlist(playlist)
      dataList.append(playlist_id.encode("ascii"))

      for item in details:
         dataList.append(item[0])
         dataList.append(str(item[1]))

      with open(dataFile, 'ab') as myfile:
         wr = csv.writer(myfile, delimiter=',')
         wr.writerow(dataList)

      print dataList

def main():
   databaseUpdate()

if __name__ == '__main__':
   main()
