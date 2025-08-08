# Multi-stage builds

hpccm allows you to define multi-stage builds, but there are some gotchas for
singularity/apptainer.


## What is it?

1. `conda.py`: hpccm recipe that creates a conda environment in the
   first stage, and copies that environment into the second stage.
1. `environment.yml`: conda environment definition file.


## How to run it?

For `singularity` format, you have to specify the `--singularity-version` option:

```bash
$ hpccm --format singularity --singularity-version 3.2 \
    --recipe conda.py --userarg environment=environment.yml \
    > conda.recipe
```
