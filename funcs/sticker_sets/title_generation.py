
def format_title(source_name: str, channel_username: str) -> str:
    # name length must be checked before
    words = source_name.split(' ')
    return ' '.join(list(filter(
        lambda x: '@' not in x,
        words
    ))) + channel_username
