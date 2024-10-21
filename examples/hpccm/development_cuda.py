'''Recipe to create either a docker container or Singularity image
for a compute node on which users can log in using password authentication.
A number of editors, git, make, CMake, GCC and Open-MPI

Usage:
    $ hpccm  --recipe development_cuda.py  --format docker
    $ hpccm  --recipe development_cuda.py  --format singularity
'''

from pathlib import Path

# Choose a base image
Stage0.baseimage('nvcr.io/nvidia/nvhpc:24.3-devel-cuda_multi-ubuntu22.04')
 
# Install CMake
Stage0 += cmake(eula=True)

# add run script, i.e., start bash
Stage0 += runscript(commands=['/bin/bash'])
