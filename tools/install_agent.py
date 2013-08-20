__author__ = 'Admin'

import os
import subprocess
import shutil
import time
import platform
import json
import urllib2


def latest_github_tag():
    """ Returns latest Release Tag at GitHub. """
    release_tags_github_url = "https://api.github.com/repos/rackerlabs/openstack-guest-agents-unix/tags"
    release_tags_json = urllib2.urlopen(release_tags_github_url)
    release_tags_data = json.load(release_tags_json)
    return str(release_tags_data[0]['name'])[1:]


def install_uuid():
    """

    :rtype : object
    """
    os.chdir("/root")
    subprocess.call(["curl", "-Lko", "uuid-1.30.tar.gz",
                     "https://pypi.python.org/packages/source/u/uuid/"
                     "uuid-1.30.tar.gz#md5=639b310f1fe6800e4bf8aa1dd9333117"])
    os.mkdir("/root/uuid")
    shutil.move("uuid-1.30.tar.gz", "/root/uuid")
    os.chdir("/root/uuid")
    subprocess.call(["tar", "-zvxf", "uuid-1.30.tar.gz"])
    time.sleep(4)
    os.chdir("/root/uuid/uuid-1.30/")
    subprocess.call(["python", "setup.py", "install"])
    os.chdir("/root")


def identify_distro():
    """
    :return:
    """
    distro = platform.dist()[0]
    return distro


def install_tar():
    """

    :rtype : object
 """
    release_tag = latest_github_tag()
    subprocess.call(["curl", "-LkO", "https://github.com/rackerlabs/openstack-guest-agents-unix/releases/download"
                                     "/v%s/nova-agent-Linux-x86_64-%s.tar.gz" % (release_tag, release_tag)])
    agent_tar_path = "/root/nova-agent/nova-agent-Linux-x86_64-%s.tar.gz" % release_tag
    nova_file = "nova-agent-Linux-x86_64-%s.tar.gz" % release_tag
    installer_path = "/root/nova-agent/"
    nova_agent__process_path = "/etc/init.d/nova-agent"
    nova_agent_path = "/usr/share/nova-agent/"

    if os.path.exists(nova_agent__process_path):
        subprocess.call(["%s" % nova_agent__process_path, "stop"])

    if os.path.exists(nova_agent_path):
        #shutil.move(nova_agent_path, "/tmp")
        subprocess.call(["rm", "-rf", "%s" % nova_agent_path])

    if not os.path.exists(installer_path):
        os.mkdir(installer_path)

    shutil.move(nova_file, installer_path)
    os.chdir(installer_path)
    subprocess.call(["tar", "-zvxf", "%s" % agent_tar_path])
    time.sleep(10)
    subprocess.call(["./installer.sh"])
    time.sleep(5)
    subprocess.call(["%s" % nova_agent__process_path, "start"])
    subprocess.call(["rm", "-rf", "%s" % installer_path])

    if 'redhat' in platform.dist():
        if int(float(platform.dist()[1])) == 5:
        #if (set(['redhat', '5.6']).issubset(set(platform.dist()))):
            install_uuid()


install_tar()
