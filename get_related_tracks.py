import spotipy
import spotify

def print_names(names):
   for name in names:
      print name

def main():
   sp = spotipy.Spotify()

   track_id = spotify.get_track_id('humble')
   artist_id = spotify.get_track_artist(track_id)

   artist_list = spotify.get_related_artists(artist_id)
   related_artists = spotify.artist_list_to_id_list(artist_list)
   
   for artist_id in related_artists:
      print(spotify.get_artist_name(artist_id) + ':')

      track_list = spotify.get_artist_top_tracks(artist_id)
      print_names(spotify.track_list_to_name_list(track_list))
       
      print('\n')
   
if __name__ == "__main__":
   main()
