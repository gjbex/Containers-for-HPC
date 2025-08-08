'''Recipe to create either a docker container or Singularity image for an image
with a conda environment.

Usage:
    $ hpccm  --recipe conda.py  --format docker  \
             --userarg environment=environment.yml
    $ hpccm  --recipe conda.py  --format singularity  \
             --singularity-version 3.2  \
             --userarg environment=environment.yml
'''

import pathlib


# Labels
labels = {
    'Maintainer': 'Geert Jan BEX',
    'Email': 'geertjan.bex@uhasselt.be',
    'Description': 'Conda environment image',
    'Version': '1.0',
}

# First stage: build the conda environment and pack it into an archive

# Choose a base image
Stage0 += baseimage(image='continuumio/miniconda3:latest', _as='build')
 
# Copy the conda environment file into the image
env_file = USERARG.get('environment', None)
if env_file is None:
    raise ValueError('The environment file must be specified using --userarg environment=environment.yml')
if not pathlib.Path(env_file).is_file():
    raise ValueError(f'The specified environment file {env_file} does not exist.')
Stage0 += copy(src=env_file, dest='/environment.yml', )

# Install conda-pack to package the conda environment
Stage0 += shell(commands=[
    'conda install -c conda-forge -y -q conda-pack',
    'conda env create -n env -q -f /environment.yml',
    'conda pack -n env -o env.tar.gz',
])

# Second stage: create the actual image with the conda environment 

# Choose a base image for the runtime environment
Stage1 += baseimage(image='debian:bullseye-slim', _as='runtime')

# Copy the packed conda environment from the first stage
Stage1 += copy(src='/env.tar.gz', dest='/env.tar.gz', _from='build')

# Unpack the conda environment
Stage1 += shell(commands=[
    'mkdir -p /env',
    'cd /env && tar xzf /env.tar.gz',
    '/env/bin/python /env/bin/conda-unpack',
    'rm /env.tar.gz',
])

# Add the conda environment to the PATH
Stage1 += environment(variables={
    'PATH': '/env/bin:$PATH',
})

# Set the default command to run when the container starts
Stage1 += runscript(commands=['bash'])

# Add labels to the final image
Stage1 += label(metadata=labels)
