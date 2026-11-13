from typing import List, Optional
from .artist import Artist


class ArtistRepository:
    """In‑memory repository for storing and retrieving Artist instances.

    This implementation is deliberately simple and thread‑unsafe, suitable for
    demonstration and unit‑testing purposes.
    """

    def __init__(self) -> None:
        self._artists: List[Artist] = []

    def add(self, artist: Artist) -> None:
        """Add a new Artist to the repository.

        Raises:
            ValueError: If an artist with the same name already exists.
        """
        if self.find_by_name(artist.name):
            raise ValueError(f"Artist with name '{artist.name}' already exists.")
        self._artists.append(artist)

    def all(self) -> List[Artist]:
        """Return a list of all stored artists."""
        # Return a copy to prevent external mutation
        return list(self._artists)

    def find_by_name(self, name: str) -> Optional[Artist]:
        """Find an artist by exact name match.

        Returns:
            The matching Artist instance, or None if not found.
        """
        for artist in self._artists:
            if artist.name == name:
                return artist
        return None
