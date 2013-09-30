#!/usr/bin/env python

import time
import os
from ConfigParser import RawConfigParser
import fabric
from fabric.api import env, run
from fabric.operations import put

branch = "tests"


def minion():
    print(">>>>>>> %s" % run('uname -s'))


def install_python_and_curl():
    try:
        #Redhat Releases
        run("if [ -f /etc/redhat-release ]; "
            "then IF_PYTHON=`which python > /dev/null ; echo $?` ; if [[ $IF_PYTHON == '1' ]]; "
            "then apt-get -y install python; fi;"
            "IF_PYTHON=`which curl > /dev/null ; echo $?` ; if [[ $IF_PYTHON == '1' ]]; "
            "then apt-get -y install curl; fi fi")

        #Open-SuSE image
        run("if [ -f /etc/SuSE-release ]; "
            "then IF_PYTHON=`which python > /dev/null ; echo $?` ; if [[ $IF_PYTHON == '1' ]]; "
            "then zypper install -y python; fi;"
            "IF_PYTHON=`which curl > /dev/null ; echo $?` ; if [[ $IF_PYTHON == '1' ]]; "
            "then zypper install -y curl; fi fi")

        #Debian images
        run("if [ -f /etc/debian_version ]; "
            "then IF_PYTHON=`which python > /dev/null ; echo $?` ; if [[ $IF_PYTHON == '1' ]]; "
            "then apt-get install -y python; fi;"
            "IF_PYTHON=`which curl > /dev/null ; echo $?` ; if [[ $IF_PYTHON == '1' ]]; "
            "then apt-get install -y curl; fi fi")

    except:
        #FreeBSD images fail for no env.shell bash
        env.shell = '/bin/csh -c'
        run("pkg_add -fr curl")
        run("pkg_add -fr python")
        run("pkg_add -fr bash")
        run("ln -sf /usr/local/bin/bash /bin/bash")
        env.shell = '/bin/bash -l -c'


def install_agent():
    run("curl -OkL https://raw.github.com/rackerlabs/openstack-guest-agents-unix/%s/tests/functional/install_agent.py" % branch)
    run("python install_agent.py")
    run("rm -rf install_agent.py")


def run_tests():
    run("curl -OkL https://raw.github.com/rackerlabs/openstack-guest-agents-unix/%s/tests/functional/agent_tester.py" % branch)
    run("python agent_tester.py")
    run("rm -rf agent_tester.py")


def install_agent_and_run_tests():
    install_python_and_curl()
    install_agent()
    print("Going for reboot")
    time.sleep(5)
    fabric.operations.reboot(120)
    run_tests()


def create_agent_tar():
    install_python_and_curl()
    run("curl -Lk https://raw.github.com/rackerlabs/openstack-guest-agents-unix/%s/tools/nova-agent-builder.sh | bash" % branch)


def install_agent_from_local_tar():
    run("curl -OkL https://raw.github.com/rackerlabs/openstack-guest-agents-unix/%s/tests/functional/install_agent.py" % branch)
    run("python install_agent.py --local /root/nova-agent/artifacts/nova-agent-FreeBSD-amd64-0.0.1.38.tar.gz")


def load_config():
    config = RawConfigParser()
    config.read(os.path.join(os.getcwd(), "fabfile.cfg"))
    env.hosts = [config.get('testnode', 'host_ipv4')]
    env.user = config.get('testnode', 'username')
    env.password = config.get('testnode', 'password')


load_config()
