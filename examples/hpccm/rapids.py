'''Recipe to create either a docker container or Singularity image
for a compute node on which users can log in using password authentication.
The SQS queue system is available as well as a number of editors, git,
make, CMake, GCC and Open-MPI

Usage:
    $ hpccm  --recipe rapids.py  --format docker
    $ hpccm  --recipe rapids.py  --format singularity
'''

from pathlib import Path

# Choose a base image
Stage0.baseimage('nvcr.io/nvidia/rapidsai/rapidsai:cuda11.2-runtime-centos7-py3.10')
 
# Install editor and other tools
Stage0 += packages(ospackages=['vim', 'less', 'ack', 'tmux'])

# Install archive and compression software and utitlies
Stage0 += packages(ospackages=['tar', 'gzip', 'bzip2', 'wget', 'ca-certificates', ])

# Install version control
Stage0 += packages(ospackages=['git', 'openssh-client', ])

# add run script, i.e., start bash
Stage0 += runscript(commands=['/bin/bash'])
