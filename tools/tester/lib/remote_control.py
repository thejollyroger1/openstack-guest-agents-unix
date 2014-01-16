#

from fabric.api import local, run, put, get, cd
from fabric.context_managers import env, settings
from fabric.tasks import execute
import fabric.network
import os

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
        fyl_name = "nova-agent-Linux-x86_64-1.39.0.tar.gz"
        this_dir = os.path.dirname(os.path.realpath(__file__)) + "/.."
        this_dir = "%s/../../.temp/artifacts" % this_dir
        this_fyl = "%s/%s" % (this_dir, fyl_name)
        that_dir = "/tmp/nova-agent"
        that_fyl = "%s/%s" % (that_dir, fyl_name)

        run("rm -rf %s; mkdir %s" % (that_dir, that_dir))
        put(this_fyl, that_fyl)
        with cd(that_dir):
            run("tar zxvf %s" % fyl_name)
            run("bash ./installer.sh")
            run("ls -la /usr/share/nova-agent")
            if run("ls /etc/init.d"):
                run("/etc/init.d/nova-agent restart")
            elif run("ls /etc/rc.d"):
                run("/etc/rc.d/nova-agent restart")
            elif run("ls /etc/systemctl"):
                run("systemctl nova-agent restart")
    fabric.network.disconnect_all()


def test_nova_agent(host, user, password, shell="bash -l -c"):
    with settings(host_string=host,
                  user=user,
                  password=password,
                  shell=shell,
                  use_ssh_config=FABRIC_USE_SSH_CONFIG,
                  warn_only=FABRIC_WARN_ONLY,
                  abort_on_prompts=FABRIC_ABORT_ON_PROMPTS):
        #install_package("python")

        fyl_name = "agent_tester.py"
        this_dir = os.path.dirname(os.path.realpath(__file__)) + "/../../../tests/automation_suite"
        this_fyl = "%s/%s" % (this_dir, fyl_name)
        that_dir = "/tmp"
        that_fyl = "%s/%s" % (that_dir, fyl_name)
        put(this_fyl, that_fyl)
        run("chmod +x %s" % that_fyl)
        run(that_fyl)


def install_package(pkg_name):
    if run("ls /etc/redhat-release"):
        run("yum install -y %s" % pkg_name)
    elif run("ls /etc/debian_version"):
        run("apt-get -y install %s" % pkg_name)
    elif run("ls /etc/gentoo-release"):
        run("emerge %s" % pkg_name)
    elif run("ls /etc/arch-release"):
        run("pacman -Sy --noconfirm %s" % pkg_name)
    elif run("ls /etc/SuSE-release"):
        run("zypper install -y %s" % pkg_name)
    elif run("ls /etc/*bsd*"):
        run("pkg_add -r %s" % pkg_name)
