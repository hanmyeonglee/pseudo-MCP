import time, datetime, random

def healthcheck():
    """Check the connection health between client and server. Always return true.

    Returns:
        boolean
    """
    return True

def server_time(is_unix: bool):
    """Give the current server time to client. If is_unix is true, than return the unix time of server and if not, than return the standard UTC time formatted time like "1970-01-01 12:34:56 UTC+0300"

    Args:
        is_unix (boolean)

    Returns:
        string
    """
    import zoneinfo
    if is_unix:
        return str(int(time.time()))
    else:
        return datetime.datetime.now(zoneinfo.ZoneInfo('Asia/Seoul')).strftime("%Y-%m-%d %H:%M:%S UTC%z")
    
def repeat_after_me(sentence: str):
    """Return the same sentence which is given by client.

    Args:
        sentence (string)

    Returns:
        string
    """
    return sentence

def random_number_generator(a: int, b: int, n: int = 1):
    """Generate array of n random numbers, n is 1 at default state. The number is integer and in the range of a and less than b. If a >= b, than return the empty array.

    Args:
        a (int)
        b (int)
        n (int, optional)

    Returns:
        array
    """
    if a >= b: return []
    return [random.randrange(a, b) for _ in range(n)]

def give_word_randomly_from_given_word_array(words: list[str]):
    """Give one random word from given words array. If array is empty, than return value is null.

    Args:
        words (array)

    Returns:
        string | null
    """
    if len(words) == 0: return None
    return random.choice(words)