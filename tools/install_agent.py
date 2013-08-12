__author__ = 'Admin'

import os
import subprocess
import shutil
import time


def install_tar():
    """


 """
    agent_tar_path = "/root/nova-agent/nova-agent-Linux-x86_64-0.0.1.37.tar.gz"
    installer_path = "/root/nova-agent/"
    nova_agent__process_path = "/etc/init.d/nova-agent"
    nova_agent_path = "/usr/share/nova-agent/"
    if os.path.exists(nova_agent_path):
        subprocess.call(["%s" % nova_agent__process_path, "stop"])

    if os.path.exists(nova_agent_path):
        shutil.move(nova_agent_path, "/tmp")

    subprocess.call(["mv", "%s" % nova_agent_path, "/tmp"])

    subprocess.call(["tar", "-zvxf", "%s" % agent_tar_path])
    time.sleep(5)
    os.chdir(installer_path)
    subprocess.call(["cd", "%s" % installer_path])
    subprocess.call(["sh", "installer.sh"])
    time.sleep(2)
    subprocess.call(["%s" % nova_agent__process_path, "start"])

install_tar()
