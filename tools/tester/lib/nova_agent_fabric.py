#

from fabric.api import local, run, put, get, cd
from fabric.context_managers import env, settings
from fabric.tasks import execute
import fabric.network
import os

import nova_agent_installer

FABRIC_USE_SSH_CONFIG = False
FABRIC_ABORT_ON_PROMPTS = False #use ENV val of NOVA_AGENT_TESTNODE_PASSWORD
FABRIC_WARN_ONLY = True


def uptime(host, user, password, shell="bash -l -c"):
    with settings(host_string=host,
                  user=user,
                  password=password,
                  shell=shell,
                  use_ssh_config=FABRIC_USE_SSH_CONFIG,
                  warn_only=FABRIC_WARN_ONLY,
                  abort_on_prompts=FABRIC_ABORT_ON_PROMPTS):
        run('uptime')
    fabric.network.disconnect_all()


def prerequisite(host, user, password, shell="bash -l -c"):
    with settings(host_string=host,
                  user=user,
                  password=password,
                  shell=shell,
                  use_ssh_config=FABRIC_USE_SSH_CONFIG,
                  warn_only=FABRIC_WARN_ONLY,
                  abort_on_prompts=FABRIC_ABORT_ON_PROMPTS):
        fyl_name = "omni-install.sh"
        this_dir = os.path.dirname(os.path.realpath(__file__)) + "/.."
        this_fyl = "%s/lib/%s" % (this_dir, fyl_name)
        that_dir = "/tmp/nova-agent"
        that_fyl = "%s/%s" % (that_dir, fyl_name)
        run("mkdir -p %s" % that_dir)
        put(this_fyl, that_fyl)
        run("chmod +x %s" % (that_fyl))
        if shell == "bash -l -c":
            run("/usr/bin/env bash %s %s" % (that_fyl, "python2"))
        else:
            run("/bin/csh %s %s %s" % (that_fyl, "python2", "bash"))
    fabric.network.disconnect_all()


def create_nova_agent_bintar(host, user, password, shell="bash -l -c"):
    with settings(host_string=host,
                  user=user,
                  password=password,
                  shell=shell,
                  use_ssh_config=FABRIC_USE_SSH_CONFIG,
                  warn_only=FABRIC_WARN_ONLY,
                  abort_on_prompts=FABRIC_ABORT_ON_PROMPTS):
        this_dir = os.path.dirname(os.path.realpath(__file__)) + "/.."
        fyl_path = "%s/../%s" % (this_dir, 'nova-agent-builder.sh')
        run("rm -rf /tmp/test_nova_agent/nova-agent; mkdir -p /tmp/test_nova_agent/nova-agent")

        put(fyl_path, "/tmp/nova-agent-builder.sh")
        run("chmod +x /tmp/nova-agent-builder.sh")
        run("/tmp/nova-agent-builder.sh")
        get("/root/nova-agent/artifacts", "%s/../../%s" % (this_dir, ".temp"))
    fabric.network.disconnect_all()


def update_nova_agent(host, user, password, shell="bash -l -c"):
    with settings(host_string=host,
                  user=user,
                  password=password,
                  shell=shell,
                  use_ssh_config=FABRIC_USE_SSH_CONFIG,
                  warn_only=FABRIC_WARN_ONLY,
                  abort_on_prompts=FABRIC_ABORT_ON_PROMPTS):
        bintar_name = "nova-agent-Linux-x86_64-1.39.0.tar.gz"
        installer_name = "nova_agent_installer.py"
        this_dir = os.path.dirname(os.path.realpath(__file__)) + "/.."
        this_bintar = "%s/../../.temp/artifacts/%s" % (this_dir, bintar_name)
        this_installer = "%s/lib/%s" % (this_dir, installer_name)
        that_dir = "/tmp/nova-agent"
        that_bintar = "%s/%s" % (that_dir, bintar_name)
        that_installer = "%s/%s" % (that_dir, installer_name)

        run("rm -rf %s; mkdir %s" % (that_dir, that_dir))
        put(this_bintar, that_bintar)
        put(this_installer, that_installer)
        run("python2 %s --local '%s'" % (that_installer, that_bintar))
    fabric.network.disconnect_all()


def test_nova_agent(host, user, password, shell="bash -l -c"):
    with settings(host_string=host,
                  user=user,
                  password=password,
                  shell=shell,
                  use_ssh_config=FABRIC_USE_SSH_CONFIG,
                  warn_only=FABRIC_WARN_ONLY,
                  abort_on_prompts=FABRIC_ABORT_ON_PROMPTS):
        new_pass = os.getenv("NOVA_AGENT_TESTNODE_PASSWORD")
        if new_pass == None:
            new_pass = "DefaultPassword"
        run("echo 'export NOVA_AGENT_TESTNODE_PASSWORD=%s' >> /etc/profile" %
           new_pass)
        run("echo $NOVA_AGENT_TESTNODE_PASSWORD")

        this_dir = os.path.dirname(os.path.realpath(__file__)) + "/../../../tests/automation_suite"
        that_dir = "/tmp/nova-agent"
        that_fyl = "%s/automation_suite/agent_tester.py" % that_dir
        run("rm -rf %s; mkdir -p %s" % (that_dir, that_dir))
        put(this_dir, that_dir)
        run("chmod +x %s" % (that_fyl))
        run(that_fyl)
    fabric.network.disconnect_all()
