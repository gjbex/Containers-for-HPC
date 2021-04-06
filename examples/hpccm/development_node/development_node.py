'''Recipe to create either a docker container or Singularity image
for a compute node on which users can log in using password authentication.
The SQS queue system is available as well as a number of editors, git,
make, CMake, GCC and Open-MPI

Usage:
    $ hpccm  --recipe compute_node.py  --format docker
    $ hpccm  --recipe compute_node.py  --format singularity
'''

from pathlib import Path


# Choose a base image
Stage0.baseimage('ubuntu:20.04')
 
# Install build tools
Stage0 += apt_get(ospackages=['build-essential', 'make'])
Stage0 += cmake(eula=True)

# Install GNU compilers (upstream)
compilers = gnu()
Stage0 += compilers

# install Open-MPI
# This is the right thing to do, but it takes forever since it actually
# builds Open MPI from source
# Stage0 += openmpi(cuda=False, infiniband=False, version='4.0.2',
#                  toolchain=compilers.toolchain, prefix='/usr/local/')
Stage0 += apt_get(ospackages=['libopenmpi-dev', 'openmpi-common', 'openmpi-bin'])

# Install debugging tools
Stage0 += apt_get(ospackages=['gdb', 'valgrind', 'strace'])

# Install some edtiors
Stage0 += apt_get(ospackages=['nano', 'vim', 'emacs', 'less'])

# Install screen sharing software
Stage0 += apt_get(ospackages=['tmux', 'screen'])

# Install version control
Stage0 += apt_get(ospackages=['git'])

# Install archive and compression software and utitlies
Stage0 += apt_get(ospackages=['tar', 'gzip', 'bzip2'])

# Copy in some example code
source_dir = Path('source-code')
example_dir = '/sample_code'
for file in source_dir.glob('*'):
    Stage0 += copy(src=f'{file}',
                   dest=f'{example_dir}/',
                   _mkdir=True)
