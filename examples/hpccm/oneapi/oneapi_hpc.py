'''Recipe to create either a docker container or Singularity image
for a compute node on which users can log in using password authentication.
The SQS queue system is available as well as a number of editors, git,
make, CMake, GCC and Open-MPI

Usage:
    $ hpccm  --recipe development_intel.py  --format docker
    $ hpccm  --recipe development_intel.py  --format singularity
'''

from pathlib import Path


# Choose a base image
Stage0.baseimage('intel/oneapi-hpckit:devel-ubuntu22.04')
 
# Install editor and other tools
Stage0 += apt_get(ospackages=['vim', 'less', 'ack', 'tmux', ])

# Install archive and compression software and utitlies
Stage0 += apt_get(ospackages=['tar', 'gzip', 'bzip2', 'wget',
                              'ca-certificates', ])

# Install version control
Stage0 += apt_get(ospackages=['git', 'openssh-client', ])

# Install debugging tools
Stage0 += apt_get(ospackages=['valgrind', 'strace', ])

# add run script, i.e., start bash
Stage0 += runscript(commands=['/bin/bash'])
