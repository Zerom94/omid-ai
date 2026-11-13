from dataclasses import dataclass


@dataclass(frozen=True)
class Artist:
    """Simple immutable data class representing a musical artist.

    Attributes:
        name: The name of the artist.
        genre: The primary musical genre associated with the artist.
    """
    name: str
    genre: str
