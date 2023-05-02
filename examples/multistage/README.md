# Multistage builds

Multi-stage builds have the advantage that libraries or tools
required for software builds in the image but not required at
runtime.  This can potentially decrease the image size
considerably.

## What is it?

1. `singlestage.def`: definition file for an statically
   build OpenMP application.
1. `multistage.def`: multistage definition file for an statically
   build OpenMP application.
1. `src`: source directory containing the OpenMP application's source
   file and the make file to build it.
