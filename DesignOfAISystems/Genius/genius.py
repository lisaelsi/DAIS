import re
import markovify

from collections import Counter
def read_lyrics():
    with open('data/eminem.txt') as f:
        lyrics_list = f.read()#.splitlines() 


    #lyrics = remove_header_footer(lyrics_list)
    return lyrics_list

def remove_header_footer(lyrics):
    lyrics.pop(0)
    print(lyrics[-1])

    for i, l in enumerate(lyrics):
        print(l)
        if 'Embed' in l:
            lyrics[i] = lyrics[i].replace('Embed', ' ')
        if '<|endoftext|>' in l:
            lyrics.pop(i)

    return lyrics

lyrics = read_lyrics()

#print(lyrics)

# Build the model
text_model = markovify.NewlineText(lyrics)

# Print five randomly generated sentences
for i in range(10):
    print(text_model.make_sentence(max_overlap_ratio=0.4, tries=1000, min_words=5, max_words=15, well_formed = False))


