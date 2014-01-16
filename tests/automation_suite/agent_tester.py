#!/usr/bin/env python

import binascii
import uuid
import subprocess
import time
import os
import re


## adopted from openstack/nova codebase
class SimpleDH(object):
    """
    This class wraps all the functionality needed to implement
    basic Diffie-Hellman-Merkle key exchange in Python. It features
    intelligent defaults for the prime and base numbers needed for the
    calculation, while allowing you to supply your own. It requires that
    the openssl binary be installed on the system on which this is run,
    as it uses that to handle the encryption and decryption. If openssl
    is not available, a RuntimeError will be raised.
    """

    def __init__(self):
        self._prime = 162259276829213363391578010288127
        self._base = 5
        self._public = None
        self._shared = None
        self.generate_private()

    def generate_private(self):
        self._private = int(binascii.hexlify(os.urandom(10)), 16)
        return self._private

    def get_public(self):
        self._public = self.mod_exp(self._base, self._private, self._prime)
        return self._public

    def compute_shared(self, other):
        self._shared = self.mod_exp(other, self._private, self._prime)
        return self._shared

    @staticmethod
    def mod_exp(num, exp, mod):
        """Efficient implementation of (num ** exp) % mod."""
        result = 1
        while exp > 0:
            if (exp & 1) == 1:
                result = (result * num) % mod
            exp = exp >> 1
            num = (num * num) % mod
        return result

    def _run_ssl(self, text, decrypt=False):
        """
        """
        _PIPE = subprocess.PIPE  # pylint: disable=E1101
        close_fds = True
        #preexec_fn = signal.signal(signal.SIGPIPE, signal.SIG_DFL)
        shell = False
        cmd = ['openssl', 'aes-128-cbc', '-A', '-a', '-pass',
               'pass:%s' % self._shared, '-nosalt']

        if decrypt:
            cmd.append('-d')
        obj = subprocess.Popen(cmd, stdin=_PIPE,
                               stdout=_PIPE, stderr=_PIPE,
                               close_fds=True)

        out, err = obj.communicate(text)

        if err:
            raise RuntimeError('OpenSSL error: %s' % err)
        return out

    def encrypt(self, text):
        return self._run_ssl(text).strip('\n')

    def decrypt(self, text):
        return self._run_ssl(text, decrypt=True)


def _call_agent_xenstore(key, val):
    """
    """
    uuid1 = uuid.uuid1()
    print(uuid1)
    print(key)
    print(val)
    subprocess.call(["xenstore-write", "data/host/%s" % uuid1, '{"name":"%s","value":"%s"}' % (key, val)])
    time.sleep(15)
    xen_read = subprocess.call(["xenstore-read", "data/guest/%s" % uuid1])
    return xen_read


def set_key_init(key):
    """
    """
    uuid1 = uuid.uuid1()
    subprocess.call(["xenstore-write", "data/host/%s" % uuid1, '{"name":"keyinit","value":"%s"}' % key])
    time.sleep(4)
    resp = subprocess.Popen(["xenstore-read", "data/guest/%s" % uuid1], stdout=subprocess.PIPE)
    out, err = resp.communicate()
    message = re.search('"([0-9]*)"', out)
    resp = message.groups()[0]
    return resp


def get_agent_version():
    """
    """
    print("Version Check")
    xen_response = _call_agent_xenstore("version", "agent")
    assert (xen_response == 0)


def reset_network():
    """
    """
    print("Performing reset network")
    xen_response = _call_agent_xenstore("resetnetwork", "")
    assert (xen_response == 0)


def reset_password():
    """
    """
    new_pass = os.getenv("NOVA_AGENT_TESTNODE_PASSWORD")
    if new_pass == None:
        new_pass = "DefaultPassword"
    dh = SimpleDH()
    args = dh.get_public()
    resp = set_key_init(args)
    agent_pub = int(resp)
    dh.compute_shared(agent_pub)
    enc_pass = dh.encrypt(new_pass + '\n')
    print ("Executing Change Password")
    xen_response = _call_agent_xenstore("password", enc_pass)
    assert (xen_response == 0)


def inject_file(file_data=None):
    """
    """
    print("Inject File")

    if file_data is None:
        file_data = "L3Jvb3QvaGVsbG8sL3Jvb3QvaGVsbG8sbm90aGluZyxlbHNlIGhlcmUgdG9vLi4g"
    xen_response = _call_agent_xenstore("injectfile", file_data)
    assert (xen_response == 0)


def curl_public_domain():
    """
    It tries to curl a Public Domain checking its IP configs and DNS resolving.
    """
    domain = "http://www.google.com"
    statuscode = subprocess.call(["curl", "-Is", "%s" % domain])
    assert (statuscode == 0)


def test_host_name():
    print("Test Host Name")
    statuscode = subprocess.call(["hostname"])
    assert (statuscode == 0)


def test_all():
    get_agent_version()
    time.sleep(2)
    reset_network()
    time.sleep(2)
    reset_password()
    inject_file()
    curl_public_domain()
    test_host_name()

if __name__ == "__main__":
    test_all()
