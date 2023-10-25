# Apps

Apptainer allows to define multiple applications in an image using `%app` sections.


## What is it?
1. `apps.def`: simple Apptainer definition file defining two applications,
   `hello` and `bye`.
1. `hello.py`, `bye.py`: Python applications to run.


## How to use?

The applications can be run by specifying the `--app` option, e.g.,
```bash
$ apptainer run  --app hello  apps.sif
$ apptainer run  --app bye  apps.sif  world
```
