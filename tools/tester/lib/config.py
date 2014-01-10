#
"""
Configurator
"""

from ConfigParser import RawConfigParser

def cloud(config_file, cloud_type):
    config = RawConfigParser()
    config.read(config_file)
    user = config.get(cloud_type, 'user')
    key = config.get(cloud_type, 'key')
    return user, key
