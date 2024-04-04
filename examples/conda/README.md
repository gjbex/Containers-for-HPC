# Conda environments

It is fairly straightforward to build an image containing a conda environment.


## What is it?

1. `conda.recipe`: Apptainer/Singularity recipe for a multistage build of an
   image that contains a conda environment.
1. `environment.yml`: conda environment description containing numpy.
1. `Dockerfile`: corresponding Docker file for the Apptainer/Singularity
   recipe.
1. `jupyterlab.recipe`: Apptainer/Singularity recipe for a multistage build of
   an image that contains a conda environment containing Jupyter Lab, as well
   as numpy and matplotlib.
1. `jupyterlab_environment.yml`: conda environment description containing
   Jupyter Lab, numpy and matplotlib.


## How to use?

After building the image as usual, the Jupyter Lab image can be started using:
```bash $ apptainer run jupyterlab.sif ``` or even: ```bash $ ./jupyterlab.sif
```

Simply open the displayed URL in your browser (provided that runs on the same
machine.
