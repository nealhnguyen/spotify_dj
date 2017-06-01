import test

def main():

   playlist = raw_input('Enter a playlist: ')

   check = test.get_playlist_tracks(playlist) #checking if the playlist exists

   while check == -1:
       playList = raw_input('Enter a valid playlist: ')
       check = test.get_playlist_tracks(playlist)

   print("Enter the feature's corresponding numbers to value (on a scale of 1-9) separated by commas: ")
   print("          5:8")
   print("      (1) - Energy\n      (2) - Liveness\n      (3) - Tempo")
   print("      (4) - Acousticness\n      (5) - Dancability\n      (6) - Valence")
   features = raw_input('')
   features = features.replace(' ', '')
   chosen_features = features.split(",")
   print chosen_features

   features_dict = dict(map(lambda s : s.split(':'), chosen_features))
   for key, value in features_dict.items():
       features_dict[key] = int(value)

   print(features_dict)
   #profile = test.makeProfile(playlist, "danceability", "acousticness", "valence", "liveness", "tempo", "energy")
   #print profile.getDetailedFeatures()

if __name__ == '__main__':
   main()
