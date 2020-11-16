# hpccm

hpccm (HPC container manager) is a tool developed by NVIDIA to define containers
using a Python script that gets translated into a Dockerfile or a Singularity
recipe.


## What is it?

1. `development_node.py`: description of a container suitable for deveopment
   with compilers for C, C++ and Fortran, as well as Open MPI.  Debugging tools
   are available as well.
1. `source-code`: directory with source code for inclusion in the image.


## How to use it?

To generate a docker file:
```bash
$ hpccm  --recipe development_node.py  --format docker  > Dockerfile
```

To generate a Singularity recipe:
```bash
$ hpccm  --recipe development_node.py  --format singularity  > development_node.def
```
