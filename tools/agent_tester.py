__author__ = 'Admin'
Author__ = 'Admin'
import uuid
import subprocess
import time


def _call_agent_xenstore(key, val):
    """
    :type key: object
    :param val:
    :param self:
    :param key:
    """
    uuid1 = uuid.uuid1()
    print(uuid1)
    print(key)
    print(val)
    subprocess.call(["xenstore-write", "data/host/%s" % uuid1, '{"name":"%s","value":"%s"}' % (key, val)])
    time.sleep(4)
    xen_read = subprocess.check_output(["xenstore-read", "data/guest/%s" % uuid1])
    print(str(xen_read))

def get_agent_version():
    """

    :rtype : object
    """
    print("Version Check")
    _call_agent_xenstore("version", "agent")


def reset_network():
    """

    :rtype : object
    """
    print("Performing reset network")
    _call_agent_xenstore("resetnetwork", "")


get_agent_version()
time.sleep(2)
reset_network()

