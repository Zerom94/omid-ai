from com.artists.artist import Artist
from com.artists.gallery import Gallery

def demo():
    gallery = Gallery()

    picasso = Artist("Pablo Picasso", 1881, 1973)
    picasso.add_work("Les Demoiselles d'Avignon", 1907)
    picasso.add_work("Guernica", 1937)

    van_gogh = Artist("Vincent van Gogh", 1853, 1890)
    van_gogh.add_work("Starry Night", 1889)
    van_gogh.add_work("Sunflowers", 1888)

    gallery.add_artist(picasso)
    gallery.add_artist(van_gogh)

    print("All artists:")
    for a in gallery.list_artists():
        print(a)

    print("\nWorks from 1889:")
    for artist_name, title in gallery.find_by_year(1889):
        print(f"{title} by {artist_name}")

if __name__ == "__main__":
    demo()
