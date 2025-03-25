# Apptainer container examples

How to use apptainer, creating images/containers, and using them.


## What is it?

1. `simple`: straightforward example of definition files.
1. `service`: example of running an apptainer image as an instance
    to provide a server.
1. `hpccm`: examples of using NVIDIA's hpccm to generate docker files and
   simgularity defintion files from a single description.
1. `apps`: illustration of defining multiple applications in a single
   image.
1. `python_scripts`: example of a container to run a Python script.
1. `cuda.recipe`: Recipe for an image that contains NVIDIA's CUDA
   development tools.  *Note:* this can only be used to run CUDA
   applications on a host system that has a CPU and has the required
   drivers installed.
1. `multistage`: example of a multistage build file.
1. `conda`: example of a multistage build of an image with a conda
   environment.
1. `reproducible_definitions`: example of using a reproducible definition
   file to build an image.
1. `apptainer_build.slurm`: Slurm script to build an image.


## How to use it?

Note that the `apptainer_build.slurm` script will only work on a VSC cluster
due to the environment variables that are set (`VSC_SCRATCH`).  Also note that
you need to adapt the script by changing the following options:

* `--account`
* `--mail-user`

Other options such as `--time` and `--cluster` can be overridden on the
command line.

To build an image, use the `apptainer` command, e.g.,

```bash
$ sbatch apptainer_build.slurm my_recipe.recipe
```
