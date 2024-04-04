# Using apptainer for development

## Motivation

Apptainer can provide and excellent environment for developers.  Although
Docker can of course be used for that purpose as well, apptainer has a number
of advantages.

* Apptainer runs under your user ID, so artifacts such as object files or
  executables are yours.
* Apptainer binds your home directory automatically as an overlay.  This means
  that your `.bashrc` and other configuration files are used in the container,
  so all your typical settings are available in a shell that runs in the
  container.
* Thanks to overlays, the current working directory can be bound transparently.
* Sharing an image is as easy as sharing a file.  Since an image is read only,
  several developers can use the same image on a shared file system.


## How to create an image?

Using NVIDIA's hpccm tool allows you to write container specifications in
Python.  This hpccm recipe can subsequently be converted to
* an apptainer recipe,
* a Dockerfile
* a Bash script.

Of course, you can write an apptainer recipe directly if you prefer, but using
hpccm seems a bit more future-proof.

Below is an example of an hpccm specification for an image to work with Intel's
OneAPI compilers.

```python '''Recipe to create either a docker container or Singularity image
for a compute node on which users can log in using password authentication.
    The SQS queue system is available as well as a number of editors, git,
    make, CMake, GCC and Open-MPI

Usage: $ hpccm  --recipe development_intel.py  --format docker $ hpccm
--recipe development_intel.py  --format singularity '''

from pathlib import Path

# Choose a base image Stage0.baseimage('intel/oneapi-hpckit:latest')
 
# Install edtior and other tools Stage0 += apt_get(ospackages=['vim', 'less',
 'ack', 'tmux', ])

# Install archive and compression software and utitlies Stage0 +=
apt_get(ospackages=['tar', 'gzip', 'bzip2', 'wget', 'ca-certificates', ])

# Install version control Stage0 += apt_get(ospackages=['git',
'openssh-client', ])

# Install debugging tools Stage0 += apt_get(ospackages=['valgrind', 'strace',
])

# add run script, i.e., start bash Stage0 += runscript(commands=['/bin/bash'])
```

This recipe uses a Docker image provided by Intel that contains the development
environment.  It adds a number of tools such as `vim`, `git` and the like to
ensure that the basic tools are available in the image.

This hpccm recipe can be translated to an apptainer recipe by running: ```bash
$ hpccm  --recipe development_intel.py  --format singularity \
      > development_intel.recipe
```

Now apptainer can be used to build the image: ```bash $ sudo apptainer build
development_intel.sif development_intel.recipe ```


## Using the image

Using the image is now straightforward, it can simply be executed: ```bash $
./development_intel.sif ``` This will work well if you are developing in (a
subdirectory of) your home directory, since the latter is bound automatically.

If that is not ghe case, you have to use apptainer's `run` command and use the
`-B` option to bind the directory, e.g., the current working directory: ```bash
$ apptainer run  -B $(pwd)  development_intel.sif ```


### Binding additional directories

It is straightforward to bind additional directories you can do this by
specifying addition bindings using `-B`, e.g., ```bash $ apptainer run  -B
/mnt/d/data:/data  development_intel.sif ``` The first directory `/mnt/d/data`,
is the one on the host, the second, `/data`, is the name of the directory in
the container.  *Note:* you an specify multiple directory bindings by adding a
`-B` option for each.


### NVIDIA GPUs

In case you need access to an NVIDIA GPU (and the host you are running it on
has one), you can simply let apptainer use underlays to get access to the
device and drivers in your container: ```bash $ apptainer run --nv
development_cuda.sif ```


### Python & R

Since apptainer will bind your home directory automatically, your host's
`.bashrc` will be sourced when the container starts.  This means that if the
latter sets a Python environment (e.g., through conda or mamba), the Python
distribution on the host will be active, and this defeats the purpose if you
have a specific Python version or packages installed in the container.  The
same applies to all packages installed in your `.R` directory.

Hence, when building an image for Python development, make sure that packages
are installed in the image, and not in your home directory.  A two-stage build
using conda may be the most convenient.  The repository contains an example of
this.
