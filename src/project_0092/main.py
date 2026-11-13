from com.artists import Artist, ArtistRepository


def main():
    repo = ArtistRepository()
    # Add some artists
    repo.add(Artist(name="Miles Davis", genre="Jazz"))
    repo.add(Artist(name="Beyoncé", genre="Pop"))
    repo.add(Artist(name="Ludovico Einaudi", genre="Classical"))

    # List all artists
    print("All artists:")
    for artist in repo.all():
        print(f"- {artist.name} ({artist.genre})")

    # Find an artist by name
    name_to_find = "Beyoncé"
    found = repo.find_by_name(name_to_find)
    if found:
        print(f"\nFound artist: {found.name} - {found.genre}")
    else:
        print(f"\nArtist '{name_to_find}' not found.")


if __name__ == "__main__":
    main()
