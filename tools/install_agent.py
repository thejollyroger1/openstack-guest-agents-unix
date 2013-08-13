__author__ = 'Admin'

import os
import subprocess
import shutil
import time
import platform


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
    agent_tar_path = "/root/nova-agent/nova-agent-Linux-x86_64-0.0.1.37.tar.gz"
    nova_file = "nova-agent-Linux-x86_64-0.0.1.37.tar.gz"
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
    time.sleep(8)
    subprocess.call(["sh", "installer.sh"])
    time.sleep(5)
    subprocess.call(["%s" % nova_agent__process_path, "start"])
    subprocess.call(["rm", "-rf", "%s" % installer_path])

    if 'redhat' in platform.dist():
        if int(float(platform.dist()[1])) == 5:
        #if (set(['redhat', '5.6']).issubset(set(platform.dist()))):
            install_uuid()


install_tar()