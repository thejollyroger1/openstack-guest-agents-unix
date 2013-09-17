__author__ = 'Shivaling Sannalli'

import httplib2 as http
import urlparse
import json
from StringIO import StringIO
import time
import ConfigParser
import logging
import os


def _http_requests(body, headers, method, url):
    ht = http.Http(disable_ssl_certificate_validation=True)
    end_point = urlparse.urlparse(url)
    response, content = ht.request(end_point.geturl(), method, body=body, headers=headers)
    return json.load(StringIO(content))


def get_auth_token(username, api_key, identity_url):
    method = 'POST'
    headers = {'Content-Type': 'application/json'}
    body = '{"auth":{"RAX-KSKEY:apiKeyCredentials":{"username":"%s", "apiKey":"%s"}}}' % (username, api_key)
    data = _http_requests(body, headers, method, "%s" % identity_url)
    return data['access']['token']['id']


def wait_server_to_active(server_id, auth_token, server_url, wait_time=0):
    """
    :param server_id:
    :param auth_token:
    :param wait_time:
    :return:
    """
    #print wait_time
    time_limit = 300
    time.sleep(20)
    url = server_url
    method = 'GET'
    headers = {'X-Auth-Token': '%s' % str(auth_token), 'Accept': 'application/json', 'Content-Type': 'application/json'}
    body = {}
    resp = _http_requests(body, headers, method, url)
    status = resp['server']['status']
    print "Server status: %s" % status
    if str(status) == 'BUILD' and wait_time < time_limit:
        wait_server_to_active(server_id, auth_token, url, wait_time + 20)
    resp = _http_requests(body, headers, method, url)
    return resp


def write_values_to_config(IPv4, admin_pass):
    config = ConfigParser.RawConfigParser()
    config.add_section('credentials')
    config.set('credentials', 'IPv4', '%s' % IPv4)
    config.set('credentials', 'username', 'root')
    config.set('credentials', 'adminpass', '%s' % admin_pass)
    with open('config.cfg', 'wb') as configfile:
        config.write(configfile)


def create_server():
    kwargs = load_configurations()
    auth_token = get_auth_token(kwargs['username'], kwargs['api_key'], kwargs['identity_url'])
    print "Auth Token: %s" % auth_token

    url = "%s" % kwargs['cloud_url'] + "%s/servers" % kwargs['tenant_id']
    method = 'POST'
    body = '{"server": {"imageRef": "%s", "flavorRef": "%s", "name": "agenttestserver"}}' \
           % (kwargs['image_id'], kwargs['flavor_id'])
    headers = {'X-Auth-Token': '%s' % str(auth_token), 'Accept': 'application/json', 'Content-Type': 'application/json'}
    resp = _http_requests(body, headers, method, url)
    print resp
    admin_pass = resp['server']['adminPass']
    server_id = resp['server']['id']
    server_url = resp['server']['links'][0]['href']
    print server_url
    print "server id: %s, password: %s" % (server_id, admin_pass)
    print "Initial wait time to get server status: 120 sec"
    time.sleep(120)
    resp = wait_server_to_active(server_id, auth_token, server_url, 0)
    print resp
    ipv4 = resp['server']['accessIPv4']
    print "IPv4 : %s" % ipv4
    write_values_to_config(ipv4, admin_pass)


def get_server_details():
    resp = wait_server_to_active("", "def6ce690bc84044a0219a92418ca16d",
                                 wait_time=0)
    ipv4 = resp['server']['accessIPv4']
    print "IPv4 : %s" % ipv4
    ipv = resp['server']['addresses']['public']
    write_values_to_config(ipv4, "Password1")


def load_configurations():
    kwargs = {}
    config = ConfigParser.RawConfigParser()
    config.read(os.path.join(os.getcwd(), "server_configurations.cfg"))
    env = config.get("environment", "name")
    print env
    kwargs['tenant_id'] = config.get("%s" % env, 'tenant_id')
    kwargs['username'] = config.get("%s" % env, "username")
    kwargs['api_key'] = config.get("%s" % env, "api_key")
    kwargs['identity_url'] = config.get("%s" % env, "identity_url")
    kwargs['cloud_url'] = config.get("%s" % env, "cloud_url")
    kwargs['image_id'] = config.get("%s" % env, "image_id")
    kwargs['flavor_id'] = config.get("%s" % env, "flavor_id")
    return kwargs


create_server()
#get_server_details()