#
"""
Virtual Machines Images
"""


def list(conn):
    """
    returns entire list of available images
    [params]
        conn: cloud connection
    """
    return conn.list_images()


def image(conn, id):
    """
    returns image object of required id
    [params]
        conn: cloud connection
        id: need to be image ID
    """
    return conn.list_images()[id]
