# hpccm

hpccm (HPC container maker) is a tool developed by NVIDIA to define containers
using a Python script that gets translated into a Dockerfile or a Singularity/apptainer
recipe.


## What is it?

1. `simple.py`: very simple example.
1. `development_base.py`: base recipe for a development container.
1. `development_c++.py`: recipe for a C++ development container.
1. `development_cuda_base.py`: base recipe for CUDA development.
1. `development_intel_base.py`: base recipe for development using
   Intel compilers.
1. `development_node`: definition of a development node.
1. `mssql_client`: defintion of a container with Microsoft
   SQL Server drivers, ODBC, FreeTDS and a conda environment
   for a client script.
1. `r_container`: definition of an image to run R.
1. `oneapi`: examples of images containing OneAPI development tools.
1 `rapids.py`: recipe for an image to run NVIDIA Rapids.
