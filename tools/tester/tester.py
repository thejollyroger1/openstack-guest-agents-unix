#!/usr/bin/env python

import sys
import os
import re
import time


import lib.provider as provider
import lib.config as config
import lib.data_handler as data_handler
import lib.virtualmachine as virtualmachine
import lib.virtualmachine_images as virtualmachine_images
import lib.virtualmachine_sizes as virtualmachine_sizes
import lib.nova_agent_fabric as nova_agent_fabric


SERVER_NAME_PREPEND = "autotest"
NODE_BUILD_TIMEOUT = 180
NODE_DATAFILE = "nodes-data.shelve"


def is_image_allowed(distro_name):
    blacklist = re.compile(r"Vyatta|Windows", re.IGNORECASE)
    if len(re.findall(blacklist, distro_name)) == 0:
        return True
    return False


def is_node_allowed(distro_name):
    whitelist = re.compile(r"%s_" % SERVER_NAME_PREPEND, re.IGNORECASE)
    if len(re.findall(whitelist, distro_name)) == 0:
        return False
    return True


def save_nodes_config(uuid, name, ip, password, shell):
    _datashelve = data_handler.DataShelve()
    _data = _datashelve.load_history(NODE_DATAFILE)
    _data[uuid] = {"name": str(name),
                   "ip": str(ip),
                   "password": str(password),
                   "shell": str(shell)}
    _datashelve.save_history(_data)


def read_nodes_config():
    _datashelve = data_handler.DataShelve()
    _data = _datashelve.load_history(NODE_DATAFILE)
    for uuid, detail in _data.items():
        print(uuid, detail, type(detail))
    _datashelve.save_history(_data)


def create_nodes(conn):
    nodes = {}
    size = virtualmachine_sizes.size(conn, 1)
    for _img in virtualmachine_images.list(conn):
        if is_image_allowed(str(_img.name)):
            print("Creating VM from image '%s' uuid:%s" % (_img.name, _img.uuid))
            vm_name = "%s_%s" % (SERVER_NAME_PREPEND,
                                 "_".join(_img.name.split()))
            metadata = virtualmachine.create(conn, vm_name, _img, size)
            print(repr(metadata))
            nodes[metadata["uuid"]] = metadata["extra"]["password"]
            print("\n")
    return nodes


def _refresh_nodes_list(selected_nodes, all_nodes):
    for _node in selected_nodes:
        try:
            _new_node = [elem for elem in all_nodes if elem.uuid == _node.uuid][0]
            selected_nodes.remove(_node)
            selected_nodes.append(_new_node)
        except:
            import pdb; pdb.set_trace()
    return selected_nodes


def get_ipv4_from_ip_list(ip_list):
    pattern = r"((([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])[ (\[]?(\.|dot)[ )\]]?){3}([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5]))"
    return [ip for ip in ip_list if re.match(pattern, ip)][0]


def _extract_node_config(nodes_to_check, nodes_password):
    nodes_checked = []
    non_bash_pattern = re.compile(r"FreeBSD.9\.2", re.IGNORECASE)
    for _node in nodes_to_check:
        if is_node_allowed(str(_node.name)):
            if _node.state == 0:
                _node_password = nodes_password[_node.uuid]
                _node_public_ip = get_ipv4_from_ip_list(_node.public_ips)
                shell = "bash -l -c"
                if re.findall(non_bash_pattern, _node.name) != []:
                    shell = "/bin/csh -c"
                save_nodes_config(_node.uuid, _node.name, _node_public_ip, _node_password, shell)
                print(str(_node.public_ips[0]))
                print("\n")
                nodes_checked.append(_node)
            elif _node.state == 3:
                print("\n\nINFO: Node %s is still building with state %s\n\n" % (_node.name, _node.state))
            else:
                print("\n\nERROR: Node '%s' seem to be in error state %s\n\n" % (_node.name, _node.state))
                nodes_checked.append(_node)
        else:
            nodes_checked.append(_node)
    return list(set(nodes_to_check) - set(nodes_checked))


def map_nodes(conn, nodes_password, datafile):
    try:
        os.remove(datafile)
    except:
        banner("%s will be created to contain node mapping" % datafile)
    nodes_to_map = conn.list_nodes()
    sleep_counter = NODE_BUILD_TIMEOUT
    while len(nodes_to_map) != 0:
        nodes_to_map = _extract_node_config(nodes_to_map, nodes_password)
        if len(nodes_to_map) != 0:
            print("Sleeping for %s seconds before re-checking for currently building nodes." % sleep_counter)
            time.sleep(sleep_counter)
            sleep_counter = sleep_counter - (sleep_counter / 2)
            nodes_to_map = _refresh_nodes_list(nodes_to_map, conn.list_nodes())


def create_bintars(datafile):
    _datashelve = data_handler.DataShelve()
    _data = _datashelve.load_history(datafile)
    whitelist_pattern = re.compile(r"CentOS.6\.5$|FreeBSD.9\.2$", re.IGNORECASE)
    bintar_nodes = [detail for uuid, detail in _data.items() if re.findall(whitelist_pattern, detail["name"]) != []]
    for detail in bintar_nodes:
        nova_agent_fabric.prerequisite(detail["ip"], "root", detail["password"], detail["shell"])
        nova_agent_fabric.create_nova_agent_bintar(detail["ip"], "root", detail["password"])
    _datashelve.save_history(_data)


def run_at_nodes(datafile, task):
    _datashelve = data_handler.DataShelve()
    _data = _datashelve.load_history(datafile)
    blacklist_pattern = re.compile(r"NOTHING", re.IGNORECASE)
    _nodes = [detail for uuid, detail in _data.items() if re.findall(blacklist_pattern, detail["name"]) == []]
    for detail in _nodes:
        task(detail)
    _datashelve.save_history(_data)


def update_nova_agent(detail):
    nova_agent_fabric.prerequisite(detail["ip"], "root", detail["password"], detail["shell"])
    nova_agent_fabric.update_nova_agent(detail["ip"], "root", detail["password"])


def test_nova_agent(detail):
    nova_agent_fabric.test_nova_agent(detail["ip"], "root", detail["password"])


def destroy_nodes(conn, datafile):
    try:
        _datashelve = data_handler.DataShelve()
        _data = _datashelve.load_history(datafile)
        blacklist_pattern = re.compile(r"NOTHING", re.IGNORECASE)
        _nodes_uuid = [uuid for uuid, detail in _data.items() if re.findall(blacklist_pattern, detail["name"]) == []]
        _datashelve.save_history(_data)

        all_nodes = conn.list_nodes()
        for _node in all_nodes:
            if _node.uuid in _nodes_uuid:
                print("Destrying instance~ uuid: %s, name: %s" %
                      (_node.uuid, _node.name))
                conn.destroy_node(_node)
        return True
    except:
        print("Destorying nodes failed.")
        return False


def banner(msg):
    print("\n||||||||||||< %s >||||||||||||\n" % msg)


if __name__ == "__main__":
    print("It's supposed to usable by fabfile only.")
    sys.exit(1)
