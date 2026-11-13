# utils.py
"""
Utility functions for fetching and formatting artist data.
"""
import json
import urllib.parse

import requests

from config import BASE_URL

def fetch_artist_data(artist_id: str) -> dict:
    """Fetch artist data from the remote service.

    Args:
        artist_id (str): The artist identifier.

    Returns:
        dict: Parsed JSON response from the server.

    Raises:
        requests.HTTPError: If the HTTP request fails.
        ValueError: If the response cannot be decoded as JSON.
    """
    params = {"artist": artist_id}
    url = f"{BASE_URL}?{urllib.parse.urlencode(params)}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    try:
        return response.json()
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON response") from exc

def format_artist_info(data: dict) -> str:
    """Create a human‑readable string from the artist data.

    The function attempts to extract common fields (name, genre, bio) but
    gracefully handles missing keys.
    """
    name = data.get("name", "Unknown Artist")
    genre = data.get("genre", "Unknown Genre")
    bio = data.get("bio", "No biography available.")
    return (
        f"Artist: {name}\n"
        f"Genre: {genre}\n"
        f"Biography:\n{bio}\n"
    )
