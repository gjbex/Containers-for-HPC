'''Recipe to create either a docker container or Singularity image
for a very simple setup

Usage:
    $ hpccm  --recipe simple.py  --format docker
    $ hpccm  --recipe simple.py  --format singularity
'''

# Choose a base image
Stage0.baseimage('ubuntu:22.04')
 
# Install editor and other tools
Stage0 += apt_get(ospackages=['vim', 'less', 'ack', 'tmux', ])

# Install archive and compression software and utitlies
Stage0 += apt_get(ospackages=['tar', 'gzip', 'bzip2', 'wget', 'ca-certificates', ])
