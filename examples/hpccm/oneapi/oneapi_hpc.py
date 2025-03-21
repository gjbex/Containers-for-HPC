'''Recipe to create either a docker container or Singularity image
for a compute node on which users can log in using password authentication.
The SQS queue system is available as well as a number of editors, git,
make, CMake, GCC and Open-MPI

Usage:
    $ hpccm  --recipe oneapi_hpc.py  --format docker
    $ hpccm  --recipe oneapi_hpc.py  --format singularity
'''

from pathlib import Path


# Choose a base image
Stage0.baseimage('intel/oneapi-hpckit:latest')
 
# Install NVIDIA backend
Stage0 += copy(src='oneapi-for-nvidia-gpus-2025.0.0-cuda-12.0-linux.sh',
            dest='/')
Stage0 += shell(commands=['/oneapi-for-nvidia-gpus-2025.0.0-cuda-12.0-linux.sh -y'])

# Install build tools
Stage0 += cmake(eula=True)

# Install editor and other tools
Stage0 += apt_get(ospackages=['vim', 'neovim', 'less', 'ack', 'tmux', ])

# Install archive and compression software and utitlies
Stage0 += apt_get(ospackages=['tar', 'gzip', 'bzip2', 'wget',
                              'ca-certificates', ])

# Install version control
Stage0 += apt_get(ospackages=['git', 'openssh-client', ])

# Install debugging tools
Stage0 += apt_get(ospackages=['valgrind', 'strace', 'cppcheck', ])

# Install benchmark tools
Stage0 += apt_get(ospackages=['hyperfine', ])

# add run script, i.e., start bash
Stage0 += runscript(commands=['/bin/bash'])
