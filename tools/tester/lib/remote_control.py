#

from fabric.api import local, run, put, get, cd
from fabric.context_managers import env, settings
from fabric.tasks import execute
import fabric.network


def uptime(host, user, password, shell="bash -l -c"):
    with settings(host_string=host,
                  user=user,
                  password=password,
                  shell=shell,
                  use_ssh_config=False,
                  warn_only=True,
                  abort_on_prompts=True):
        run('uptime')
    fabric.network.disconnect_all()


def create_nova_agent_bintar(host, user, password, shell="bash -l -c"):
    with settings(host_string=host,
                  user=user,
                  password=password,
                  shell=shell,
                  use_ssh_config=False,
                  warn_only=True,
                  abort_on_prompts=True):
        import os
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
                  use_ssh_config=False,
                  warn_only=True,
                  abort_on_prompts=True):
        import os
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
