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
def makeProfile(playlistName, feat1, feat2, feat3, feat4, feat5, feat6):
    value1 = 0
    value2 = 0
    value3 = 0
    value4 = 0
    value5 = 0
    value6 = 0

    track_list = []

    track_list = get_playlist_tracks(playlistName)
    for (name, trackId) in track_list:
       features = get_track_features(trackId)
       for feature in features:
         value1 += feature[feat1]
         value2 += feature[feat2]
         value3 += feature[feat3]
         value4 += feature[feat4]
         value5 += feature[feat5]
         value6 += feature[feat6]

    avg1 = value1/len(track_list)
    avg2 = value2/len(track_list)
    avg3 = value3/len(track_list)
    avg4 = value4/len(track_list)
    avg5 = value5/len(track_list)
    avg6 = value6/len(track_list)
    

    profile = Profile(feat1, avg1, feat2, avg2, feat3, avg3, feat4, avg4, feat5, avg5, feat6, avg6)
    return profile

#'''
##example: making a profile
#print "Printing initial profile 1 stats..."
#print profile1.getDetailedFeatures()
#print "Making profile 1 w/ the playlist Happy Hits!..."
#profile1 = makeProfile("Happy Hits!", "danceability", "acousticness", "valence")
#print "Updated values: "
#print profile1.getDetailedFeatures()
#'''
#
##comparing the profiles of the two playlists
##def compareProfile(userPlaylist, topPlaylist):
#
##create profile for each of these top playlists
#playlists = ["Hot Rhythmic", "Good Vibes", "RapCaviar", "Chill Hits", 
#        "electroNOW", "Hot Country", "Rock This", "Are & Be", 
#        "Today's Top Hits", "Weekly Buzz", "Have A Great Day", "Relax & Unwind", "Most Necessary", "Signed XOXO", 
#         "Pop Chillout", "Beach Vibes", "Fresh Electronic", "New Boots", 
#         "New Noise", "Totally Alternative", 
#          "Gold Edition", "Teen Party", "Get Turnt", "Ultimate Indie", "State of Jazz", "The Piano Bar"]
#for playlist in playlists:
#    profile = makeProfile(playlist, "energy", "liveness", "tempo")
#    print playlist
#    print profile.getDetailedFeatures()
#
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
   profile = Profile("danceability", 0.6693300000000002, "acousticness", 0.13855849999999992, "valence", 0.4957969999999998)

   with open('data.csv', 'rb') as csvFile:
      for row in csvFile:
         listValues = row.split(",")
         
         name = listValues[0]
         acousticness = listValues[listValues.index("acousticness") + 1]
         danceability = listValues[listValues.index("danceability") + 1][:-2]
         valence = listValues[listValues.index("valence") + 1]
         tempProfile = Profile("danceability", float(danceability), "acousticness", float(acousticness), "valence", float(valence))

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

               tempProfile = Profile("danceability", value1, "acousticness", value2, "valence", value3)
               sim = compareProfile(profile, tempProfile)
               if  sim >= .990:
                  count += 1
                  print name, " ", compareProfile(profile, tempProfile) 

               if count >= 5:
                  break

if __name__ == '__main__':
   main()
