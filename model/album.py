from dataclasses import dataclass

@dataclass
class Album:
    AlbumId : int
    Title : str
    ArtistId : int

    def __hash__(self):
        return hash(self.ArtistId)

    def __eq__(self, other):
        return self.ArtistId == other.ArtistId

    def __str__(self):
        return f"{self.Title} di {self.ArtistId}, codice: {self.AlbumId}"

    