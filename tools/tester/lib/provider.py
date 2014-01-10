#
"""
Cloud Provider Connections
"""

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver


CloudProviders = {
    'bluebox': Provider.BLUEBOX,
    'brightbox': Provider.BRIGHTBOX,
    'cloudsigma': Provider.CLOUDSIGMA,
    'cloudstack': Provider.CLOUDSTACK,
    'dreamhost': Provider.DREAMHOST,
    'ec2': Provider.EC2,
    'joyent': Provider.JOYENT,
    'libvirt': Provider.LIBVIRT,
    'linode': Provider.LINODE,
    'opennebula': Provider.OPENNEBULA,
    'openstack': Provider.OPENSTACK,
    'opsource': Provider.OPSOURCE,
    'rackspace': Provider.RACKSPACE,
    'rackspace-nova-dfw': Provider.RACKSPACE_NOVA_DFW,
    'slicehost': Provider.SLICEHOST
}


def connection(user, key, cloud):
    """
    [param]
        "user": <username for account>,
        "key": <api key for given account>,
        "cloud": <key name of target cloud>
    """
    try:
        Driver = get_driver(CloudProviders[cloud])
        return Driver(user, key)
    except Exception, e:
        print("Connection failed.\n%s" % e)
        import sys
        sys.exit(127)
