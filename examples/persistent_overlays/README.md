# Persisntent overlays

Persistent overlays allow to overlay a writable filesystem while building or running a container.


## What is it?

1. `r_container.py`: hpccm recipe file to build a container with R installed.
1. `r_container.recipe`: Singularity recipe file to build a container with R installed.

## How to use it?

Create thé overlay directory:
```bash
$ mkdir overlay_dir/
```

Create the image:
```bash
$ apptainer build r_container.sif r_container.recipe
```

Use the overlay:
```bash
$ apptainer exec --overlay overlay_dir/ r_container.sif /bin/bash
```
