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
Stage0 += apt_get(ospackages=['software-properties-common', 'apt-transport-https', 'dirmngr', 'gnupg'])

# Add signature key for CRAN
Stage0 += shell(commands=['wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc | tee -a /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc'])

# Add CRAN repository
Stage0 += shell(commands=['add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/"'])

# Install build tools
Stage0 += apt_get(ospackages=['build-essential', 'make'])
Stage0 += cmake(eula=True)

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

# Set environment variables
Stage0 += environment(variables={'LC_ALL': 'C.UTF-8'})
Stage0 += environment(variables={'TZ': 'Europe/Brussels'})
