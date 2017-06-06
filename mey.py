import test
import classes

def UserInput():
   
   sp = classes.Spotify()

   user_playlist = raw_input('Enter a playlist name:')
   
   check = sp.search_playlist(user_playlist) #checking if the playlist exists
   
   while check == -1:
      playList = raw_input('Enter a valid playlist: ')
      check = sp.search_playlist(user_playlist)
   
   print("Enter the feature's corresponding numbers to value (on a scale of 1-9) separated by commas: ")
   print("  Ex. Dancability with the value 8 would be 5:8")
   print("      (1) - Energy\n      (2) - Liveness")
   print("      (3) - Acousticness\n      (4) - Dancability\n      (5) - Valence")
   features = raw_input('')
   features = features.replace(' ', '')
   chosen_features = features.split(",")
   
   features_dict = dict(map(lambda s : s.split(':'), chosen_features))
   for key, value in features_dict.items():
      features_dict[key] = int(value)



   userPreferredFeat = {}

   for key, value in features_dict.items():
      featName = numToFeature[key]
      userPreferredFeat[featName] = int(value)

   return user_playlist, userPreferredFeat

if __name__ == '__main__':
   UserInput()
