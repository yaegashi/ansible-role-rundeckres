#!/usr/bin/env python

import sys, os, json

if len(sys.argv) < 2:
    print "Usage: %s <facts_dir>" % sys.argv[0]
    quit()

factdir = sys.argv[1]

a = []
for i in os.listdir(factdir):
    if not i.endswith(".json"):
        continue
    with open("%s/%s" % (factdir, i)) as f:
        j = json.load(f)
        b = {
            "nodename": j['inventory_hostname'],
            "hostname": j['ansible_hostname'],
            "username": j['rundeckres_username'],
            "tags": ','.join(j['group_names']),
            "osFamily": j['ansible_system'],
            "osArch": j['ansible_architecture'],
            "osName": j['ansible_distribution'],
            "osVersion": j['ansible_distribution_version'],
        }
        if 'ansible_lsb' in j:
            b['description'] = j['ansible_lsb']['description']
        else:
            b['description'] = "%s %s" % (j['ansible_distribution'],
                                          j['ansible_distribution_version'])
        a.append(b)

json.dump(a, sys.stdout, indent=2)
