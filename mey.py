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










if __name__ == '__main__':
   main()
