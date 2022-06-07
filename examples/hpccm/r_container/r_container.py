'''Recipe to create either a docker container or Singularity image
to perform data processing and rendering for the DSI covid-19
dashboard.

Usage:
    $ hpccm  --recipe dashboard.py  --format docker
    $ hpccm  --recipe dashboard.py  --format singularity
'''

from pathlib import Path


# Choose a base image
Stage0.baseimage('ubuntu:21.04')
 
# Install build tools
Stage0 += apt_get(ospackages=['build-essential', 'make'])

# Install libraries
Stage0 += apt_get(ospackages=['openssl', 'libxml2-dev', 'libcurl4-openssl-dev', 'libz-dev', 'libssl-dev',
                              'libjpeg-dev', ])
# Install GNU compilers (upstream)
compilers = gnu()
Stage0 += compilers

# install GDAL library
Stage0 += apt_get(ospackages=['libgdal-dev', 'libudunits2-dev'])

# Install utilities
Stage0 += apt_get(ospackages=['gist', 'wget', 'rclone', ])

# Install BLAS and Lapack
Stage0 += apt_get(ospackages=['libopenblas-dev', 'liblapack-dev'])

# Install R
Stage0 += apt_get(ospackages=['r-base', ])

# Install R packages
Stage0 += copy(src='install_packages.R', dest='/setup/', _mkdir=True)
Stage0 += shell(commands=['Rscript /setup/install_packages.R'])
