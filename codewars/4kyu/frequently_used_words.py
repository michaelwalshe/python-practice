import re
from collections import Counter

def top_3_words(text):
    # Escape for the empty/no letters case
    if not any(c.isalpha() for c in text):
        return []
    
    # Case insensitive
    text = text.lower()
    # If it isn't a letter or an apostrophe, it's whitespace
    clean_text = re.sub(r"[^a-zA-Z\']+", " ", text)
    # Split into words on whitespace
    words = clean_text.split()
    # Get the 3 most common words
    word_freq = Counter(words).most_common(3)
    # Just return the words, not the frequencies
    return [word_tup[0] for word_tup in word_freq]