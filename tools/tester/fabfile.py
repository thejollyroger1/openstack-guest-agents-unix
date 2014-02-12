#!/usr/bin/env python


import tester
import sys


def create_nodes(config_file):
    cloud_type = "rackspace-nova-dfw"

    user, key = tester.config.cloud(config_file, cloud_type)
    conn = tester.provider.connection(user, key, cloud_type)

    tester.banner("CREATE NODES")
    nodes_password = tester.create_nodes(conn)

    tester.banner("MAP CREATED NODES TO CONFIG")
    tester.map_nodes(conn, nodes_password, tester.NODE_DATAFILE)


def destroy_nodes(config_file):
    cloud_type = "rackspace-nova-dfw"

    user, key = tester.config.cloud(config_file, cloud_type)
    conn = tester.provider.connection(user, key, cloud_type)

    tester.banner("Destroying Nodes")
    tester.destroy_nodes(conn, tester.NODE_DATAFILE)


def read_nodes():
    tester.banner("READ NODES CONFIG")
    tester.read_nodes_config()


def create_bintars():
    tester.banner("CREATE BINTARs")
    tester.create_bintars(tester.NODE_DATAFILE)


def update_nova_agent():
    tester.banner("UPDATE NOVA AGENT")
    tester.run_at_nodes(tester.NODE_DATAFILE, tester.update_nova_agent)


def test_nova_agent():
    tester.banner("TEST NOVA AGENT")
    tester.run_at_nodes(tester.NODE_DATAFILE, tester.test_nova_agent)


def ls_nova_agent():
    tester.banner("UPDATE NOVA AGENT")
    tester.run_at_nodes(tester.NODE_DATAFILE,
                        tester.nova_agent_fabric.ls_nova_agent)


def uptime():
    tester.banner("UPDATE NOVA AGENT")
    tester.run_at_nodes(tester.NODE_DATAFILE, tester.nova_agent_fabric.uptime)


def create_update_test(config_file):
    create_nodes(config_file)
    create_bintars()
    update_nova_agent()
    test_nova_agent()


if __name__ == "__main__":
    print("Run me using fabric. To see available commands, run: `fab -l`")
    sys.exit(1)
