#!/usr/bin/env python3
"""
Entry point for the artist data fetcher.
"""

import argparse
import sys

from client import fetch_artist_data
from config import BASE_URL

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch artist information from a PHP endpoint.")
    parser.add_argument(
        "artist_id",
        type=int,
        help="Numeric ID of the artist to retrieve (e.g., 1)",
    )
    parser.add_argument(
        "--output",
        "-o",
        choices=["json", "text"],
        default="text",
        help="Format of the displayed output.",
    )
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    try:
        data = fetch_artist_data(args.artist_id)
    except Exception as exc:
        print(f"Error fetching artist data: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.output == "json":
        import json
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        # Pretty‑print selected fields
        name = data.get("name", "N/A")
        genre = data.get("genre", "N/A")
        albums = data.get("albums", [])
        print(f"Artist: {name}")
        print(f"Genre: {genre}")
        print("Albums:")
        for album in albums:
            title = album.get("title", "Unknown")
            year = album.get("year", "???")
            print(f"  • {title} ({year})")

if __name__ == "__main__":
    main()
