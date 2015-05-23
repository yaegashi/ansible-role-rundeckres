#!/usr/bin/env python

import sys, os, json

OSARCH_DICT = { 'x86_64': 'amd64', 'i386': 'x86' }
OSFAMILY_DICT = { '/': 'unix', '\\': 'windows' }

if len(sys.argv) < 2:
    print 'Usage: %s <facts_dir>' % sys.argv[0]
    quit()

factsdir = sys.argv[1]

a = []
for i in os.listdir(factsdir):
    if not i.endswith('.json'):
        continue
    with open('%s/%s' % (factsdir, i)) as f:
        node = os.path.splitext(i)[0]
        try:
            j = json.load(f)
            a_system = j.get('ansible_system', '')
            a_architecture = j.get('ansible_architecture', '')
            a_kernel = j.get('ansible_kernel', '')
            a_os_family = j.get('ansible_os_family', '')
            a_distribution = j.get('ansible_distribution', '')
            a_distribution_version = j.get('ansible_distribution_version', '')
            a_distribution_major_version = j.get('ansible_distribution_major_version', '')
            a_distribution_release = j.get('ansible_distribution_release', '')
            if 'ansible_lsb' in j:
                a_description = j['ansible_lsb']['description']
            else:
                a_description = '%s %s' % (a_distribution,
                                           a_distribution_version)
            b = {
                'nodename': j.get('inventory_hostname', node),
                'hostname': j.get('ansible_hostname', node),
                'username': j.get('rundeckres_username', ''),
                'tags': ','.join(j.get('group_names', [])),
                'description': a_description,

                # osXXX attributes are based on Rundeck core API source,
                # namly NodeSupport#createFrameworkNode().
                # osName: System.getProperty("os.name")
                'osName': a_system,
                # osArch: System.getProperty("os.arch")
                'osArch': OSARCH_DICT.get(a_architecture, a_architecture),
                # osVersion: System.getProperty("os.version")
                'osVersion': a_kernel,
                # osFamily: Path separator '/' for "unix", '\\' for "windows"
                'osFamily': OSFAMILY_DICT.get(os.sep, ''),

                # ansibleXXX attributes are simply derived from Ansible facts.
                'ansibleOsFamily': a_os_family,
                'ansibleDistribution': a_distribution,
                'ansibleDistributionVersion': a_distribution_version,
                'ansibleDistributionMajorVersion': a_distribution_major_version,
                'ansibleDistributionRelease': a_distribution_release,
            }
            c = dict([(k, v) for k, v in b.items() if v.strip()])
            a.append(c)
        except Exception as x:
            b = {
                'nodename': node,
                'hostname': node,
                'rundeckresError': str(x),
            }
            a.append(b)

json.dump(a, sys.stdout, indent=2)
