# Reproducible definitions

Defintion of a reproducible image to run R with specific versions
of packages.

## What is it?

1. `r_container.py`: hpccm definition of the image.
1. `install_packages.R`: R script to install additional libraries.
1. `r_container.recipe`: Singularity/Apptainer recipe to build the image,
   generated from `r_container.py` using hpccm.
