class Gallery:
    def __init__(self):
        self.artists = {}

    def add_artist(self, artist):
        self.artists[artist.name] = artist

    def get_artist(self, name):
        return self.artists.get(name)

    def list_artists(self):
        return list(self.artists.values())

    def find_by_year(self, year):
        result = []
        for artist in self.artists.values():
            for work in artist.works:
                if work["year"] == year:
                    result.append((artist.name, work["title"]))
        return result
