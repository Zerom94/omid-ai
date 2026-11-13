import requests
from urllib.parse import urljoin, urlencode

from config import BASE_URL, TIMEOUT

def build_url(artist_id: int) -> str:
    """Construct the full request URL for a given artist ID."""
    query = urlencode({"artist": artist_id})
    return urljoin(BASE_URL, f"php?{query}")

def fetch_artist_data(artist_id: int) -> dict:
    """
    Retrieve artist information from the remote PHP endpoint.

    Parameters
    ----------
    artist_id: int
        The numeric identifier of the artist.

    Returns
    -------
    dict
        Parsed JSON response from the server.

    Raises
    ------
    requests.HTTPError
        If the HTTP request fails or returns a non‑200 status.
    ValueError
        If the response cannot be decoded as JSON.
    """
    url = build_url(artist_id)
    response = requests.get(url, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()
