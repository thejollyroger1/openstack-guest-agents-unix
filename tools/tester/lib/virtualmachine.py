#
"""
CRUD Virtual Machines
"""

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

import lib.virtualmachine_images as virtualmachine_images
import lib.virtualmachine_sizes as virtualmachine_sizes


def create(conn, name, image, size):
    """
    conn, name, image, size
    """
    node = conn.create_node(name=name, image=image, size=size)

    return {"uuid": node.uuid,
            "id": node.id,
            "extra": node.extra,
            "private_ips": node.private_ips,
            "public_ips": node.public_ips,
            "state": node.state}


def create_by_id(conn, name, image_id, size_id):
    """
    conn, name, image_id, size_id
    """
    node = conn.create_node(name=name,
                            image=virtualmachine_images.image(conn, image_id),
                            size=virtualmachine_sizes.size(conn, size_id))

    return {"uuid": node.uuid,
            "id": node.id,
            "extra": node.extra,
            "private_ips": node.private_ips,
            "public_ips": node.public_ips,
            "state": node.state}

