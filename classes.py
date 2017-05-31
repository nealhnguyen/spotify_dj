class Song:
    def __init__(self, profile):
        self.profile = profile

class Playlist:
    def __init__(self, profile):
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


