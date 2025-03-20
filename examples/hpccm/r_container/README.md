# R container

Defintion of an image to run R.

## What is it?

1. `r_container.py`: hpccm definition of the image.
1. `r_container.recipe`: Singularity/Apptainer definition of the image,
   generated from `r_container.py` using hpccm.
1. `install_packages.R`: R script to install additional libraries.
