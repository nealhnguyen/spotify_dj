from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import spotify
import json
import csv
from math import*
from decimal import Decimal
from scipy import spatial
from classes import Profile 
from classes import Song
from classes import Playlist

#results = spotify.search_by_artist_name('kanye west')
#artists = results['artists']
#artists = artists['items']

#artistId = artists[0]['id']
#relatedArtists = spotify.get_related_artists(artistId)

client_credentials_manager = SpotifyClientCredentials(client_id = 'a64e7ced0f1d40c0960a9f13608c4e37', client_secret = '139896904200432696a1ffda522daa7e')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace=False

scaleFactor = 10
requiredSim = .995
tracksPerList = 5

def get_track_features(trackID):
   features = sp.audio_features(trackID)
   return (features)

def get_playlist_tracks(playlistName):
   track_list = []
   results = sp.search(q=playlistName, type='playlist')
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

#make a profile given a specific playlist name and the features that we want to use
def makeProfile(playlistName, feat1, feat2, feat3):
    variance = 0
    value1 = 0
    value2 = 0
    value3 = 0
    track_list = []

    track_list = get_playlist_tracks(playlistName)
    for (name, trackId) in track_list:
       features = get_track_features(trackId)
       for feature in features:
         value1 += feature[feat1]
         value2 += feature[feat2]
         value3 += feature[feat3]

    avg1 = value1/len(track_list)
    avg2 = value2/len(track_list)
    avg3 = value3/len(track_list)
    
    print("Made a profile")

    profile = Profile(variance, feat1, avg1, feat2, avg2, feat3, avg3)
    return profile

def squareRooted(x):
   return round(sqrt(sum([a * a for a in x])), 3)
  
def cosineSimilarity(x,y):
   numerator = sum(a * b for a, b in zip(x,y))
   denominator = squareRooted(x) * squareRooted(y)
   return round(numerator / float(denominator), 3)

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

   return cosineSimilarity(vector1, vector2)

def main():
#   playList = raw_input('Enter a playlist: ')
#   print playList
#   profile = makeProfile(playList, "danceability", "acousticness", "valence")
#   print profile.getDetailedFeatures()

   # Pop Rising
   profile = Profile(7, "danceability", 0.6693300000000002, "acousticness", 0.13855849999999992, "valence", 0.4957969999999998)

   with open('data.csv', 'rb') as csvFile:
      for row in csvFile:
         listValues = row.split(",")
         
         name = listValues[0]
         acousticness = listValues[listValues.index("acousticness") + 1]
         danceability = listValues[listValues.index("danceability") + 1][:-2]
         valence = listValues[listValues.index("valence") + 1]
         tempProfile = Profile(7, "danceability", float(danceability), "acousticness", float(acousticness), "valence", float(valence))

         similarity = compareProfile(profile, tempProfile)
         
         if similarity >= requiredSim:
            print "Name: ", name, " Similarity: ", similarity

            count = 0
            tracks = get_playlist_tracks(name)
            for name, trackId in tracks:
               features = get_track_features(trackId)
               for feature in features:
                  value1 = feature["danceability"]
                  value2 = feature["acousticness"]
                  value3 = feature["valence"]

               tempProfile = Profile(7, "danceability", value1, "acousticness", value2, "valence", value3)
               sim = compareProfile(profile, tempProfile)
               if  sim >= .990:
                  count += 1
                  print name, " ", compareProfile(profile, tempProfile) 

               if count >= 5:
                  break

if __name__ == '__main__':
   main()
