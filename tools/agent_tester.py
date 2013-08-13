__author__ = 'Admin'
Author__ = 'Admin'
import uuid
import subprocess
import time
import platform
import os
import shutil


def install_uuid():
    """

    :rtype : object
    """
    subprocess.call("curl -Lko uuid-1.30.tar.gz "
                    "https://pypi.python.org/packages/source"
                    "/u/uuid/uuid-1.30.tar.gz#md5=639b310f1fe6800e4bf8aa1dd9333117")
    os.mkdir("/root/uuid")
    shutil.move("uuid-1.30.tar.gz", "/root/uuid")
    os.chdir("/root/uuid")
    subprocess.call(["tar", "-zvxf", "uuid-1.30.tar.gz"])
    time.sleep(4)
    os.chdir("/root/uuid/uuid-1.30/")
    subprocess.call("python setup.py install")


def _call_agent_xenstore(key, val):
    """
    :type key: object
    :param val:
    :param self:
    :param key:
    """

    if 'redhat' in platform.dist():
        if int(float(platform.dist()[1])) == 5:
    #if (set(['redhat', '5.6']).issubset(set(platform.dist()))):
            install_uuid()

    uuid1 = uuid.uuid1()
    print(uuid1)
    print(key)
    print(val)
    subprocess.call(["xenstore-write", "data/host/%s" % uuid1, '{"name":"%s","value":"%s"}' % (key, val)])
    time.sleep(8)
    xen_read = subprocess.call(["xenstore-read", "data/guest/%s" % uuid1])
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

