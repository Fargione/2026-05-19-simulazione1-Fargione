from dataclasses import dataclass

@dataclass
class MediaType:
    MediaTypeId : int
    Name : str

    def __hash__(self):
        return hash(self.MediaTypeId)

    def __eq__(self, other):
        return self.MediaTypeId == other.MediaTypeId

    def __str__(self):
        return f"{self.MediaTypeId}"