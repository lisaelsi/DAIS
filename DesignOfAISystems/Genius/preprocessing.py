
import re
import markovify


def read_lyrics():
    with open('data/eminem-large.txt') as f:
        lyrics = f.read()
        
    return lyrics

lyrics = read_lyrics()

words = re.split("\W+", lyrics)

words = [word.lower() for word in words]

lyrics = " ".join(words)

# Build the model
text_model = markovify.NewlineText(lyrics)

print(lyrics)

# Print five randomly generated sentences
for i in range(10):
    print(text_model.make_sentence(max_overlap_ratio=0.4, tries=10, min_words=5, max_words=15))

