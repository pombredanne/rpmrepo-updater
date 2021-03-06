#!/usr/bin/env python

# This is a script to remove packages from all repos quickly.  It will prompt to show what would happen (using listfilter) and the remove using removefilter. 

from __future__ import print_function
import argparse
import subprocess
import sys
import time

DISTROS = ['precise', 'quantal', 'raring', 'saucy', 'trusty']
REPOS = ['/var/www/repos/building', '/var/www/repos/ros-shadow-fixed/ubuntu', '/var/www/repos/ros/ubuntu',]

import argparse

parser = argparse.ArgumentParser(description='Find and remove packages from ROS repos.')
parser.add_argument('regex',
                   help='the regex to use in reprepro')
args = parser.parse_args()

def apply_command_template(repo, command_arg, distro, regex):
    command_template = '/usr/bin/reprepro -b %(repo)s -V %(command_arg)s %(distro)s' % locals()
    _cmd = command_template.split() + [regex]
    print("Running %s" % _cmd)
    subprocess.Popen(_cmd)
    # sleep to let the lock file cleanup before iterating
    time.sleep(1)
    

for repo in REPOS:
    for distro in DISTROS:
        apply_command_template(repo, 'listfilter', distro, args.regex)


confirmation = raw_input('Would you like to remove these packages? If so type "yes":')

if confirmation != "yes":
    print('You did not enter "yes" exiting.')
    sys.exit(1)

for repo in REPOS:
    for distro in DISTROS:
        apply_command_template(repo, 'removefilter', distro, args.regex)
