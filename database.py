import spotipy
import spotify
import csv
from spotipy.oauth2 import SpotifyClientCredentials
from classes import Profile
from test import makeProfile

dataFile = "data3.csv"

client_credentials_manager = SpotifyClientCredentials(client_id = 'a64e7ced0f1d40c0960a9f13608c4e37', client_secret = '139896904200432696a1ffda522daa7e')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace=False

def databaseUpdate():
   playlists = ["Hot Rhythmic", "Good Vibes", "RapCaviar", "Chill Hits", "electroNOW", "Hot Country", "Rock This", "Are & Be"]
   playlists += ["Pop Rising", "Have a Great Day!", "Most Necessary", "Pop Chillout", "dancePop", "New Boots", "New Noise", "The Newness", "Teen Party", "Morning Accoustic"]
   for playlist in playlists:
      profile = makeProfile(playlist, "danceability", "acousticness", "valence", "energy", "liveness", "tempo")
      dataList = []
      details = profile.features.items() 

      dataList.append(playlist)
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
