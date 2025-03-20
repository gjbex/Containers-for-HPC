'''Recipe to create either a docker container or Singularity image
for computations using R.

Usage:
    $ hpccm  --recipe r_container.py  --format docker
    $ hpccm  --recipe r_container.py  --format singularity
'''

# Choose a base image
Stage0.baseimage('ubuntu:22.04')
 
# Install tools to install R
Stage0 += apt_get(ospackages=[
    'software-properties-common=0.99.22.9',
    'apt-transport-https=2.4.13',
    'dirmngr=2.2.27-3ubuntu2.1',
    'gnupg=2.2.27-3ubuntu2.1', 'wget',
])

# Add signature key for CRAN
Stage0 += shell(commands=['wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc | tee -a /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc'])
Stage0 += shell(commands=['apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 51716619E084DAB9'])

# Add CRAN repository
Stage0 += shell(commands=['add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/"'])

# Install build tools
Stage0 += apt_get(ospackages=['build-essential=12.9ubuntu3', 'make=4.3-4.1build1'])
Stage0 += cmake(eula=True, version='3.22.1')

# Install GNU compilers (upstream)
Stage0 += apt_get(ospackages=['g++=4:11.2.0-1ubuntu1', 'gfortran=4:11.2.0-1ubuntu1'])

# Install libraries required to build R
Stage0 += apt_get(ospackages=['openssl=3.0.2-0ubuntu1.19', 'libxml2-dev=2.9.13+dfsg-1ubuntu0.6', 'libcurl4-openssl-dev=7.81.0-1ubuntu1.20', 'libz-dev', 'libssl-dev=3.0.2-0ubuntu1.19',
                              'libjpeg-dev=8c-2ubuntu10', ])
# Install BLAS and Lapack
Stage0 += apt_get(ospackages=['libopenblas-dev=0.3.20+ds-1', 'liblapack-dev=3.10.0-2ubuntu1'])

# Install R
Stage0 += apt_get(ospackages=['r-base=4.4.3-1.2204.0', ])

# installing libraries required by R packages, e.g., GDAL library
Stage0 += apt_get(ospackages=[
    'libgdal-dev=3.4.1+dfsg-1build4',
    'libudunits2-dev=2.2.28-3',
    'libfontconfig1-dev=2.13.1-4.2ubuntu5',
    'libharfbuzz-dev=2.7.4-1ubuntu3.2',
    'libfribidi-dev=1.0.8-2ubuntu3.1',
])

# Install R packages
Stage0 += copy(src='install_packages.R', dest='/setup/', _mkdir=True)
Stage0 += shell(commands=['Rscript /setup/install_packages.R'])

# Include the R scripts and data, stored locally in the Code-main directory
# Stage0 += copy(src='Code-main/', dest='/workspace/', _mkdir=True)

# Set environment variables
Stage0 += environment(variables={'LC_ALL': 'C.UTF-8'})
Stage0 += environment(variables={'TZ': 'Europe/Brussels'})
