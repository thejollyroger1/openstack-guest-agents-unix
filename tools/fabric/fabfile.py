#!/usr/bin/env python

import os
import ConfigParser
from fabric.api import local, env, run


def load_configs():
    config_file = './fabfile.cfg'
    if not os.path.exists(config_file):
        config_file = raw_input("Enter path for config file: ")

    config = ConfigParser.RawConfigParser()
    config.read(config_file)
    
    hosts = config.get('infrastructure', 'host_ips').split('\n')
    hosts.remove('')
    user = config.get('credentials', 'user')
    password = config.get('credentials', 'password')

    env.hosts = hosts
    env.user = user
    env.password = password


def uptime():
    run('uptime')


def create_nova_agent_bintar():
    github = 'https://raw.github.com/rackerlabs/openstack-guest-agents-unix'
    branch = 'master'
    fyl_path = 'tools/nova-agent-builder.sh'
    run('curl -Lk %s/%s/%s | bash' % (github, branch, fyl_path))


def update_nova_agent():
    run('echo "to-be-done"')
    pass


# mandatory
load_configs()
