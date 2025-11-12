from dataclasses import dataclass
from typing import List
import core.models.music as models


@dataclass
class Artist:
    id: str
    name: str
    spotify_url: str

    @staticmethod
    def from_json(json: dict) -> "Artist":
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
    def spotify_uri(self) -> str:
        return self.id

    @staticmethod
    def from_json(json: dict) -> "Track":
        return Track(
            json["uri"],
            json["name"],
            [Artist.from_json(artist) for artist in json["artists"]],
            json["album"]["images"][0]["url"],
            json["external_urls"]["spotify"],
            json["preview_url"],
        )

    @staticmethod
    def from_model(model: models.Track) -> "Track":
        return Track(
            str(model.id),
            model.title,
            list(
                map(
                    lambda artist: Artist(str(artist.id), artist.name, ""),
                    model.artists.all(),
                )
            ),
            model.image_url if model.image_url else "",
            "",
            model.preview_url if model.preview_url else "",
        )
