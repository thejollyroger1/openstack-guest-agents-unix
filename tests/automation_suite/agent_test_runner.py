#!/usr/bin/env python

import time
import os
from ConfigParser import RawConfigParser
import fabric
from fabric.api import env, run
from fabric.operations import put
from tools import server_creator


branch = os.getenv("NOVA_AGENT_BRANCH")
if not branch:
    branch = "master"

local_base = os.getenv("NOVA_AGENT_LOCALBASE")
if not local_base:
    local_base = os.path.join("/tmp", "nova-agent", branch)


def load_config():
    fabfile = server_creator.create_server(120)
    config = RawConfigParser()
    config.read(os.path.join(os.getcwd(), fabfile))
    hosts = config.get('credentials', 'ipv4')
    user = config.get('credentials', 'username')
    print(user, hosts)
    env.host_string = user + "@" + hosts
    env.password = config.get('credentials', 'adminpass')


def prerequisite():
    install_prerequisite = os.path.join(local_base, "install_prerequisite.sh")
    try:
        run("mkdir -p %s" % local_base)
        put(install_prerequisite, install_prerequisite)
        run("bash %s %s" % (install_prerequisite, "python"))
    except:
        env.shell = "/bin/csh -c"
        run("mkdir -p %s" % local_base)
        put(install_prerequisite, install_prerequisite)
        run("/bin/csh %s %s %s" % (install_prerequisite, "python", "bash"))
        env.shell = "bash -l -c"


def run_n_remove(filename, run_as):
    _path_dir, _path_fyl = local_base, os.path.join(local_base, filename)

    run("mkdir -p %s" % _path_dir)
    put(_path_fyl, _path_fyl)

    run("%s %s" % (run_as, _path_fyl))
    run("rm -f %s" % _path_fyl)


def install_agent():
    run_n_remove("install_agent.py", "python")


def run_tests():
    run_n_remove("agent_tester.py", "python")


def install_agent_and_run_tests():
    load_config()
    prerequisite()
    install_agent()
    print("Going for reboot")
    time.sleep(5)
    fabric.operations.reboot(120)
    run_tests()


load_config()
if __name__ == "__main__":
    install_agent_and_run_tests()
