#
"""
"""

import os
import socket
import urllib2

import nova_test_toolset as novaci


def check_resolv(url):
    try:
        dns = socket.gethostbyname(url)
        return True
    except Exception, e:
        return False


def check_http(url):
    req = urllib2.Request(url)
    try: urllib2.urlopen(req)
    except Exception, e:
        if(str(e.reason) == "[Errno -2] Name or service not known"):
            return False
    return True


def check_resolv_conf():
    resolv_conf = "/etc/resolv.conf"
    if novaci.is_system_command("resolvconf") and os.path.islink(resolv_conf):
        return True
    if os.path.isfile(resolv_conf):
        return True
    return False
