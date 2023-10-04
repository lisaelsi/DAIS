import lyricsgenius as lg
file = open("./test.txt", "w")
from my_secrets import client_access_token

genius = lg.Genius(client_access_token, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True, timeout=100)

def get_lyrics(arr, k):
    c = 0
    for name in arr:
        try:
            songs = (genius.search_artist(name, max_songs=k, sort='popularity')).songs
            s = [song.lyrics for song in songs]
            file.write("\n \n \n \n".join(s))
            c += 1
            print(f"Songs grabbed:{len(s)}")
        except Exception as e:
            print(f"some exception at {name}: {c}")
            print(e)

artist = ['Eminem']

get_lyrics(artist, 50)