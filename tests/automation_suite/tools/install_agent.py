#!/usr/bin/env python
"""
to install latest release nova-agent from GitHub
$ ./install_agent.py

to install a specific release version from GitHub
$ ./install_agent.py --version <XX.YY.ZZ.NN>

to install a specific release version from another absolute URL
$ ./install_agent.py --url <http://URL>

to install a specific release version from already uploaded TGZ
$ ./install_agent.py --local <local/path>
"""

import os
import sys
import subprocess
import shutil
import time
import platform
import urllib2

distro_name = platform.dist()[0]
distro_family = platform.system()


def panic(msg):
    """ To do suitable task on PANIC state, Exit and Call for help. """
    print(msg)
    sys.exit(1)


def run_me_right(cmd):
    """ Run what is asked for and Panic if it fails. """
    print("Running: %s" % cmd)
    statuscode = subprocess.call(cmd.split())
    if statuscode != 0:
        panic("FAILURE: %s" % cmd)


def latest_github_tag():
    """ Returns latest Release Tag at GitHub. """
    release_tag = os.getenv("NOVA_AGENT_RELEASE")
    if release_tag:
        return release_tag

    import json
    release_tags_github_url = "https://api.github.com/repos/rackerlabs/openstack-guest-agents-unix/tags"
    release_tags_json = urllib2.urlopen(release_tags_github_url)
    release_tags_data = json.load(release_tags_json)
    return str(release_tags_data[0]['name'])[1:]


def download_link(link, to_file=""):
    """ Curls down the link to a specific filename if provided or default. """
    if to_file:
        switch = "--create-dirs -skLo"
    else:
        switch = "-skL"
    run_me_right("curl %s %s %s" % (switch, to_file, link))


def install_uuid():
    """ Installing UUID package for Testing purpose. """
    version = "1.30"
    base_path = "/tmp/uuid"
    if os.path.exists(base_path):
        run_me_right("%s stop" % base_path)

    tar_name = "uuid-%s.tar.gz" % (version)
    tar_path = "%s/%s" % (base_path, tar_name)

    md5 = "md5=639b310f1fe6800e4bf8aa1dd9333117"
    tar_url = "https://pypi.python.org/packages/source/u/uuid/uuid"
    tar_url = "%s-%s.tar.gz#%s" % (tar_url, version, md5)

    download_link(tar_url, tar_path)

    os.chdir(base_path)
    run_me_right("tar zvxf %s" % (tar_name))
    time.sleep(4)
    os.chdir("%s/uuid-%s/" % (base_path, version))
    run_me_right("python setup.py install")


class Nova:
    def agent_remove(self, service_path):
        """ Cleans up curret Nova Agent. """
        if os.path.exists(service_path):
            run_me_right("%s stop" % service_path)

        paths_to_remove = ["/usr/share/nova-agent/",
                          "/usr/sbin/nova-agent",
                          service_path]

        for path in paths_to_remove:
            if os.path.exists(path):
                run_me_right("rm -rf %s" % path)

    def agent_install(self, **kwargs):
        """ Cleans and Install latest agent. """
        if 'version' in kwargs:
            version = kwargs['version']
        else:
            version = 'custom'

        if (distro_family == 'Linux'):
            service_path = "/etc/init.d/nova-agent"
            tar_name = "nova-agent-Linux-x86_64-%s.tar.gz" % version
        elif (distro_family == 'FreeBSD'):
            run_me_right("pkg_add -fr bash")
            service_path = "/etc/rc.d/nova-agent"
            tar_name = "nova-agent-FreeBSD-amd64-%s.tar.gz" % version
        else:
            panic("Distro Family '%s' is not supported." % distro_family)


        if 'local' in kwargs:
            tar_base_path, tar_name = os.path.split(kwargs['local'])
        else:
            tar_base_path = "/root/nova-agent"
            tar_path = "%s/%s" % (tar_base_path, tar_name)

            if 'url' in kwargs:
                tar_url = kwargs['url']
            else:
                git_url = "https://github.com/rackerlabs/openstack-guest-agents-unix"
                tar_url = "%s/releases/download/v%s/%s" % (git_url, version, tar_name)
            download_link(tar_url, tar_path)

        self.agent_remove(service_path)

        os.chdir(tar_base_path)
        run_me_right("tar zvxf %s" % (tar_name))
        time.sleep(5)
        run_me_right("bash installer.sh")
        time.sleep(5)
        run_me_right("%s start" % service_path)

        if 'redhat' in platform.dist():
            if int(float(platform.dist()[1])) == 5:
                install_uuid()


def install_nova_agent():
    """
    Install nova_agent from github-latest-release, another url or local path
    based tar file, using command line switches.
    """
    config_key = sys.argv[1]
    if config_key == '--version':
        Nova().agent_install(version=sys.argv[2])
        return
    elif config_key == '--url':
        Nova().agent_install(url=sys.argv[2])
        return
    elif config_key == '--local':
        Nova().agent_install(local=sys.argv[2])
        return

    Nova().agent_install(version=latest_github_tag())


if __name__ == "__main__":
    install_nova_agent()
