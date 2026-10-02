'''Recipe to create either a docker container or Singularity image
for development with the NVIDIA HPC SDK.
A number of utilities are also installed.

Usage:
    $ hpccm  --recipe nvidia_hpc_sdk.py  --format docker
    $ hpccm  --recipe nvidia_hpc_sdk.py  --format singularity
'''

from pathlib import Path

# Choose a base image
Stage0.baseimage('nvcr.io/nvidia/nvhpc:26.3-devel-cuda_multi-ubuntu22.04')

# Install CMake
Stage0 += cmake(eula=True)

# Install editor and other tools
Stage0 += apt_get(ospackages=[
    'vim',
    'less',
    'ack',
    'tar',
    'gzip',
    'bzip2',
    'wget',
    'ca-certificates', 
    'git',
    'openssh-client',
    'valgrind',
    'strace',
    'hyperfine',
])

# add run script, i.e., start bash
Stage0 += runscript(commands=['/bin/bash'])
