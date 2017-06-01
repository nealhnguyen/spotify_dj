import test

def main():

   playList = raw_input('Enter a playlist: ')

   check = test.get_playlist_tracks(playList) #checking if the playlist exists

   while check == -1:
       playList = raw_input('Enter a valid playlist: ')
       check = test.get_playlist_tracks(playList)

   print("Enter the feature's corresponding numbers separated by commas: ")
   print("      (1) - Energy\n      (2) - Liveness\n      (3) - Tempo")
   print("      (4) - Acousticness\n      (5) - Dancability\n      (6) - Valence")
   features = raw_input('')

   chosen_features = [int(s, 10) for s in features.split(",")] #this is a list of numbers

   profile = test.makeProfile(playlist, "danceability", "acousticness", "valence", "liveness", "tempo", "energy")
   print profile.getDetailedFeatures()



'''def get_playlist_tracks(playlistName):
   track_list = []
   results = sp.search(q=playlistName, type='playlist')
   check = results['playlists']['total']
   if check == 0 :
      return -1
   else :
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

      return track_list'''






if __name__ == '__main__':
   main()
