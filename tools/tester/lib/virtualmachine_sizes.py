#
"""
Virtual Machines Sizes
"""


def list(conn):
    """
    returns list of all available sizes
    [params]
        conn: cloud connection
    """
    return conn.list_sizes()


def size(conn, id):
    """
    returns size filtered by required id
    [params]
        conn: cloud connection
        id: need to be image ID
    """
    return conn.list_sizes()[id]
