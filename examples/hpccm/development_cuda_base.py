'''Recipe to create either a docker container or Singularity image
for a compute node on which users can log in using password authentication.
A number of editors, git, make, CMake, GCC and Open-MPI

Usage:
    $ hpccm  --recipe development_cuda.py  --format docker
    $ hpccm  --recipe development_cuda.py  --format singularity
'''

from pathlib import Path

# Choose a base image
Stage0.baseimage('nvcr.io/nvidia/nvhpc:23.11-devel-cuda_multi-ubuntu22.04')
 
# Install CMake
Stage0 += cmake(eula=True)

# Install editor and other tools
Stage0 += apt_get(ospackages=['vim', 'less', 'ack', 'tmux', ])

# Install archive and compression software and utitlies
Stage0 += apt_get(ospackages=['tar', 'gzip', 'bzip2', 'wget', 'ca-certificates', ])

# Install version control
Stage0 += apt_get(ospackages=['git', 'openssh-client', ])

# Install debugging tools
Stage0 += apt_get(ospackages=['valgrind', 'strace', ])

# Install benchmarking tools
Stage0 += apt_get(ospackages=['hyperfine'])

# add run script, i.e., start bash
Stage0 += runscript(commands=['/bin/bash'])
