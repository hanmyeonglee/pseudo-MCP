import time, datetime

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

