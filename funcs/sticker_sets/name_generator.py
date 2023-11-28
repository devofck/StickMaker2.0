import random


def create_uniq_name() -> str:
    symbols = 'abcdefghijklnopqrstuvwxyz'
    symbols += symbols.upper()
    symbols += '1234567890'
    res = ''
    for _ in range(8):
        res += random.choice(symbols)
    res += '_by_in_progress_bot'
    return res


def random_file_name(file_format: str) -> str:
    return ('temp/' +
            str(random.randint(1000000, 9999999)) +
            file_format)


def get_random_emojis():
    emoji_list = '😀😃😄😁😆🥹😅😂🤣🥲☺️😊😇🙂🙃😉😌😍🥰😘😗😙😚😋😛😝😜🤪🤨🧐🤓😎🥸🤩🥳😏😒😞😔😟😕🙁'
    res = []
    for _ in range(15):
        res.append(random.choice(emoji_list))

    return res
