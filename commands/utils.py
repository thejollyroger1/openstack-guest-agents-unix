# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
#  Copyright (c) 2011 Openstack, LLC.
#  All Rights Reserved.
#
#     Licensed under the Apache License, Version 2.0 (the "License"); you may
#     not use this file except in compliance with the License. You may obtain
#     a copy of the License at
#
#          http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#     WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#     License for the specific language governing permissions and limitations
#     under the License.
#

"""
utils module with common utility set commands
"""

# Utilities:
    # - is_system_command(<command_name>) : boolean for command in system exec path

import sys
import logging
import subprocess

def is_system_command(cmd):
    return subprocess.call("type " + cmd,
                           shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE
                          ) == 0


def run_without_error(cmd):
    logging.info("Calling '%s'" % cmd)
    try:
        status = subprocess.call(cmd.split())
        logging.info("'%s' exited with code %d" % (cmd, status))
        if status == 0:
            return True
    except:
        logging.info("'%s' raised exception" % cmd)
    return False
