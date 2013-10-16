#
"""
"""

import subprocess


def is_system_command(cmd):
    return subprocess.call("type " + cmd,
                           shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE
                          ) == 0
