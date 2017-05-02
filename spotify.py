import requests

GET_ARTIST_ENDPOINT = 'https://api.spotify.com/v1/artists/{id}'
SEARCH_ENDPOINT = 'https://api.spotify.com/v1/search'
RELATED_ARTISTS_ENDPOINT = 'https://api.spotify.com/v1/artists/{id}/related-artists'
TOP_TRACKS_ENDPOINT = 'https://api.spotify.com/v1/artists/{id}/top-tracks'
AUDIO_FEATURE = 'https://api.spotify.com/v1/audio-features/{id}'

def get_artist(artist_id):
   url = GET_ARTIST_ENDPOINT.format(id=artist_id)
   resp = requests.get(url)
   return resp.json()

def search_by_artist_name(name):
   myparams = {'type': 'artist'}
   myparams['q'] = name
   resp = requests.get(SEARCH_ENDPOINT, params=myparams)
   return resp.json()

def get_related_artists(artist_id):
   url = RELATED_ARTISTS_ENDPOINT.format(id=artist_id)
   resp = requests.get(url)
   return resp.json()

def get_artist_top_tracks(artist_id, country='US'):
   url = TOP_TRACKS_ENDPOINT.format(id=artist_id)
   myparams = {'country': country}
   resp = requests.get(url, params=myparams)
   return resp.json()

def get_audio_features(track_id, country='US'):
   url = AUDIO_FEATURE.format(id=track_id)
   resp = requests.get(AUDIO_FEATURE)
   return resp.json()
