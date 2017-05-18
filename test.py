from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import spotify
import json

class Song:
    def __init__(self, title, profile):
        self.title = title
        self.profile = profile

class Playlist:
    def __init__(self, title, profile):
        self.title = title
        self.profile = profile

class Profile:
    'Common profile class for all playlists'
    def __init__(self, variance, feat1, val1, feat2, val2, feat3, val3):
        self.features = {}
        self.features[feat1] = val1
        self.features[feat2] = val2
        self.features[feat3] = val3

        self.variance = variance

    def edit(self, variance, feat1, val1, feat2, val2, feat3, val3):
        self.variance = variance
        self.features[feat1] = val1
        self.features[feat2] = val2
        self.features[feat3] = val3

    def getTopFeatures(self):
        allKeys = self.features.keys()
        for key in allKeys:
            print(key)
        print('\n')

    def getDetailedFeatures(self):
        details = self.features.items()
        for item in details:
            print(item)
        print('\n')


results = spotify.search_by_artist_name('kanye west')
artists = results['artists']
artists = artists['items']

artistId = artists[0]['id']
relatedArtists = spotify.get_related_artists(artistId)

client_credentials_manager = SpotifyClientCredentials(client_id = 'a64e7ced0f1d40c0960a9f13608c4e37', client_secret = '139896904200432696a1ffda522daa7e')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace=False

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
       if not (song['track']['id'] is None):
          track_list.append(song['track']['id'].encode('utf-8'))
   return track_list


#hardcode
'''
danceability = 0
acousticness = 0
valence = 0
track_list = []
playlistName = raw_input("Enter playlist name: ")
get_playlist_tracks(playlistName)
for track in track_list:
   features = get_track_features(track)
   for feature in features:
     danceability += feature['danceability']
     acousticness += feature['acousticness']
     valence += feature['valence']
avgDanceability = danceability/len(track_list)
avgAcousticness = acousticness/len(track_list)
avgValence = valence/len(track_list)
print "The number of songs in this playlist is: " + str(len(track_list))
print "The average dancability is: " + str(avgDanceability)
print "The average acousticness is: " + str(avgAcousticness)
print "The average valence is: " + str(avgValence)
'''

#make a profile given a specific playlist name and the features that we want to use
def makeProfile(playlistName, feat1, feat2, feat3):

    variance = 0
    value1 = 0
    value2 = 0
    value3 = 0
    track_list = []

    track_list = get_playlist_tracks(playlistName)
    for track in track_list:
       features = get_track_features(track)
       for feature in features:
         value1 += feature[feat1]
         value2 += feature[feat2]
         value3 += feature[feat3]

    avg1 = value1/len(track_list)
    avg2 = value2/len(track_list)
    avg3 = value3/len(track_list)

    profile = Profile(variance, feat1, avg1, feat2, avg2, feat3, avg3)
    return profile


#example: making a profile
profile1 = makeProfile("Happy Hits!", "danceability", "acousticness", "valence")
print "Printing features: "
print profile1.getTopFeatures()
print profile1.getDetailedFeatures()
