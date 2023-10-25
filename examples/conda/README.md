# Conda environments

It is fairly straightforward to build an image containing a conda
environment.


## What is it?

1. `conda.recipe`: Apptainer/Singularity recipe for a multistage
   build of an image that contains a conda environment.
1. `environment.yml`: conda environment description containing
   numpy.
1. `Dockerfile`: corresponding Docker file for the Apptainer/Singularity
   recipe.
