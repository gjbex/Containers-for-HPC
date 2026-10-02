'''Recipe to create either a docker container or Singularity image
for a compute node on which users can log in using password authentication.
The SQS queue system is available as well as a number of editors, git,
make, CMake, GCC and Open-MPI

Usage:
    $ hpccm  --recipe conda.py  --format docker
    $ hpccm  --recipe conda.py  --format singularity
'''

# Choose a base image
Stage0.baseimage('ubuntu:22.04')

# Create Python environment with conda
c = conda(eula=True, environment='environment.yml')
Stage0 += c

Stage1 += baseimage(image='debian:bullseye-slim', _as='runtime')
Stage1 += c.runtime()
# ensure that .local is ignored
Stage1 += environment(variables={'PYTHONNOUSERSITE': '1', })
