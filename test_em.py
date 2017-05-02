import spotify

def getRelatedArtists(name):
    results = spotify.search_by_artist_name(name)
    artists = results['artists']
    artists = artists['items']
    id = artists[0]['id']
    related_artists = spotify.get_related_artists(id)

    artistList = []
    for a in related_artists['artists']:
        artistList.append(a['name']) 

    return artistList 

def getArtistId(name):
    results = spotify.search_by_artist_name(name)
    artists = results['artists']
    artists = artists['items']
    return artists[0]['id']

def getTopTracks(id, country='US'):
    results = spotify.get_artist_top_tracks(id, country)
    topTracks = results['tracks']

    tracks = []
    for track in topTracks: 
        tracks.append(track['name'])
        print(track['name'])

    return tracks

artist = input("Who's your favorite artist?")
artistList = getRelatedArtists(artist)
print('If you like {0}...\n'.format(artist))

artistId = getArtistId(artist)
getTopTracks(artistId)

for name in artistList:
    print(name + ':\n')
    artistId = getArtistId(name)
    getTopTracks(artistId)
    print('\n')
