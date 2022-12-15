'''Recipe to create either a docker container or Singularity image
for computations using R.

Usage:
    $ hpccm  --recipe r_container.py  --format docker
    $ hpccm  --recipe r_container.py  --format singularity
'''

# Choose a base image
Stage0.baseimage('ubuntu:22.04')
 
# Install utilities
Stage0 += apt_get(ospackages=['gist', 'wget', 'rclone', ])

# Install build tools
Stage0 += apt_get(ospackages=['build-essential', 'make'])

# Install GNU compilers (upstream)
compilers = gnu()
Stage0 += compilers

# Install libraries required to build R
Stage0 += apt_get(ospackages=['openssl', 'libxml2-dev', 'libcurl4-openssl-dev', 'libz-dev', 'libssl-dev',
                              'libjpeg-dev', ])
# Install BLAS and Lapack
Stage0 += apt_get(ospackages=['libopenblas-dev', 'liblapack-dev'])

# Install R
Stage0 += apt_get(ospackages=['r-base', ])

# installing libraries required by R packages, e.g., GDAL library
Stage0 += apt_get(ospackages=['libgdal-dev', 'libudunits2-dev'])

# Install R packages
Stage0 += copy(src='install_packages.R', dest='/setup/', _mkdir=True)
Stage0 += shell(commands=['Rscript /setup/install_packages.R'])
