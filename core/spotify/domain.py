from dataclasses import dataclass
from typing import List


@dataclass
class Artist:
    id: str
    name: str
    spotify_url: str

    @staticmethod
    def from_json(json):
        return Artist(
            json["uri"], json["name"], json["external_urls"]["spotify"]
        )


@dataclass
class Track:
    id: str
    track_name: str
    track_artists: List[Artist]
    image: str
    spotify_url: str
    preview_url: str

    @property
    def spotify_uri(self):
        return self.id

    @staticmethod
    def from_json(json):
        return Track(
            json["uri"],
            json["name"],
            [Artist.from_json(artist) for artist in json["artists"]],
            json["album"]["images"][0]["url"],
            json["external_urls"]["spotify"],
            json["preview_url"],
        )

    @staticmethod
    def from_model(model):
        return Track(
            model.id,
            model.title,
            list(
                map(
                    lambda artist: Artist(artist.id, artist.name, ""),
                    model.artists.all(),
                )
            ),
            "",
            "",
            "",
        )
