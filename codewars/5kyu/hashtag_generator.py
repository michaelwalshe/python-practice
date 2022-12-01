def generate_hashtag(s):
    if not s:
        return False
    hashtag = s.title().replace(' ', '')

    if len(hashtag) == 0 or len(hashtag) > 140:
        return False
    else:
        return f"#{hashtag}"
        