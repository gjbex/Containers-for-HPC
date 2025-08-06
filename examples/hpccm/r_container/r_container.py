'''Recipe to create either a docker container or Singularity image
for computations using R.

Usage:

To produce the base image:
    $ hpccm  --recipe r_container.py  --format singularity  \
             --userarg apt_list=apt_packages.txt  \
                       r_package_install=install_r_packages.R

To create an image based on the base image, but with additional packages installed:
    $ hpccm  --recipe r_container.py  --format singularity  \
             --userarg apt_list=apt_packages.txt  \
                       r_package_install=install_r_packages.R
                       bootstrap=localimage  \
                       baseimage=base_image.sif

Note that in this case, apt_packages.txt should only contain packages that are not already
installed in the base image, so it can be an empty file.
             --
'''

# import required modules
import pathlib

# Get the list of apt packages to install
apt_list_filename = USERARG.get('apt_list', 'apt_packages.txt')
if not pathlib.Path(apt_list_filename).is_file():
    raise FileNotFoundError(f"File {apt_list_filename} not found.")
with open(apt_list_filename, 'r') as apt_file:
    apt_packages = [line.strip() for line in apt_file if line.strip()]

r_package_install_filename = USERARG.get('r_package_install', 'install_packages.R')
if not pathlib.Path(r_package_install_filename).is_file():
    raise FileNotFoundError(f"File {r_package_install_filename} not found.")

# Get the base image
image = USERARG.get('baseimage', 'ubuntu:22.04')

# Get the bootstrap method
bootstrap = USERARG.get('bootstrap', 'docker')
if bootstrap not in ['docker', 'localimage']:
    raise ValueError("Bootstrap method must be either 'docker' or 'localimage'.")

if bootstrap == 'localimage':
    # If using a local image, make sure it exists
    if not pathlib.Path(image).is_file():
        raise FileNotFoundError(f"Local image file {image} does not exist.")

# Choose a base image
Stage0 += baseimage(image=image, _bootstrap=bootstrap)
 
# Install apt packages
if apt_packages:
    Stage0 += apt_get(ospackages=apt_packages)

# Add CRAN repository and signature key
if bootstrap == 'docker':
    Stage0 += shell(commands=['wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc | tee -a /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc'])
    Stage0 += shell(commands=['add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/"'])
    Stage0 += shell(commands=['apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 51716619E084DAB9'])

# Install CMake and compiler suite
if bootstrap == 'docker':
    Stage0 += cmake(eula=True)
    Stage0 += gnu()

# Install R
if bootstrap == 'docker':
    Stage0 += apt_get(ospackages=[
        'r-base',
        'r-base-dev',
        'r-cran-biocmanager',
    ])

# Install R packages
Stage0 += copy(src=r_package_install_filename, dest='/setup/', _mkdir=True)
Stage0 += shell(commands=[f'Rscript /setup/{r_package_install_filename}'])

# Set environment variables
Stage0 += environment(variables={'LC_ALL': 'C.UTF-8'})
Stage0 += environment(variables={'TZ': 'Europe/Brussels'})

# Add runtime script
Stage0 += runscript(commands=['Rscript'])
