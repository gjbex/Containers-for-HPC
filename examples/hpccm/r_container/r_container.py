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

# Install tools to install R
Stage0 += apt_get(ospackages=[
    'software-properties-common',
    'apt-transport-https',
    'dirmngr',
    'gnupg',
])

# Add signature key for CRAN
Stage0 += shell(commands=['wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc | tee -a /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc'])

# Add CRAN repository and signature key
Stage0 += shell(commands=['add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/"'])
Stage0 += shell(commands=['apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 51716619E084DAB9'])

# Install build tools and compilers
Stage0 += apt_get(ospackages=[
    'build-essential',
    'make',
])
Stage0 += cmake(eula=True)
Stage0 += gnu()

# Install HDF5 libraries
Stage0 += hdf5(configure_opts=['--enable-cxx', '--enable-fortran',])

# Install libraries required to build R
Stage0 += apt_get(ospackages=[
    'openssl',
    'libxml2-dev',
    'libcurl4-openssl-dev',
    'libz-dev', 'libssl-dev',
    'libjpeg-dev',
])

# Install BLAS and Lapack
Stage0 += apt_get(ospackages=[
    'libopenblas-dev',
    'liblapack-dev',
])

# Install R
Stage0 += apt_get(ospackages=['r-base', ])

# Installing libraries required by R packages, e.g., GDAL library,
# required for spatial data processing
Stage0 += apt_get(ospackages=[
    'libgdal-dev',
    'libudunits2-dev',
])

# Install libraries required by tidyverse
Stage0 += apt_get(ospackages=[
    'libfontconfig1-dev',
    'libharfbuzz-dev',
    'libfribidi-dev',
])

# Install R packages
Stage0 += copy(src='install_packages.R', dest='/setup/', _mkdir=True)
Stage0 += shell(commands=['Rscript /setup/install_packages.R'])

# Set environment variables
Stage0 += environment(variables={'LC_ALL': 'C.UTF-8'})
Stage0 += environment(variables={'TZ': 'Europe/Brussels'})

# Add runtime script
Stage0 += runscript(commands=['R'])
