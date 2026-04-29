Apptainer, previously known as Singularity, can be viewed as Docker for HPC:
an image can contain the operating system and software components for your
application and can be deployed and run on HPC infrastructure, as well as on
your own laptop, and even in the cloud.

An additional advantage of containers is that they can help you create a
software environment that is stable over long periods of time, which helps
reproduce results in the future.


## Learning outcomes

When you complete this training you will be able to

  * use Apptainer containers on HPC systems;
  * create your own definition files for containers;
  * understand strengths and weaknesses of containers;
  * recognize and avoid potential pitfalls.


## Schedule

Total duration: 3 hours.

  | Subject                             | Duration |
  |-------------------------------------|----------|
  | introduction and motivation         | 15 min.  |
  | Apptainer definition files          | 75 min.  |
  | coffee break                        | 15 min.  |
  | Apptainer and parallel applications | 15 min.  |
  | Apptainer and services              | 20 min.  |
  | hands-on                            | 30 min.  |
  | wrap up                             | 10 min.  |


## Training materials

Slides are available in the
 [GitHub repository](https://github.com/gjbex/Containers-for-HPC/),
as well as example container definition files.


## Target audience

This training is for you if you have non-trivial workflows on HPC systems or
reproducibility requirements and want to use containers effectively.


## Prerequisites

You should be comfortable using Linux and the HPC environment.
If necessary, attend the appropriate training sessions on those subjects first.

More concretely, participants should already be comfortable with the following:

* logging in to an HPC system and working from the shell;
* navigating directories, creating and editing files, and running commands from
  the command line;
* understanding the difference between login nodes and compute nodes;
* submitting and monitoring basic batch jobs if image builds or runs need to be
  done through Slurm;
* working with software environments at a user level, for example modules,
  compilers, or Python environments;
* reading and making small changes to short shell scripts.

Familiarity with Docker concepts is helpful, but not strictly required.
You do not need prior experience with Apptainer or Singularity, container
definition files, multi-stage builds, or HPC-oriented container tools such as
hpccm. Those are part of the training itself.

### Quick self-assessment

If you can do most of the tasks below without looking up basic Linux or HPC
syntax, you are likely ready for this training.

* log in to an HPC cluster and move to the directory where your files are
  stored;
* edit a short text file or shell script and run a command from that directory;
* understand where a job should run: on the login node or on a compute node;
* submit a basic Slurm job and check whether it is queued, running, or
  finished;
* read a short shell script and identify the input file, output file, and main
  command being executed;
* understand at a high level why packaging software and dependencies together
  can help reproducibility;
* make a small change to a recipe or script and rerun it.

If several of these items still feel difficult, the training will probably move
too fast. In that case, it is better to first refresh Linux command-line use
and basic HPC job handling.

### Software and access requirements

To follow along hands-on, you need
* laptop or desktop with internet access and set up so you can connect to an
  HPC system;
* an account on an HPC system (e.g., VSC, CECI, ...);
* compute credits if that is required to run jobs on the HPC system;


## Level of the Material

For participants who already have basic Linux and HPC experience, the material
in this training is approximately

* Introductory: 25 %
* Intermediate: 55 %
* Advanced: 20 %

These percentages describe the level of the container and reproducibility
topics covered in the training, not the required entry level in Linux or HPC
usage itself.


## Trainer(s)

  * Geert Jan Bex ([geertjan.bex@uhasselt.be](mailto:geertjan.bex@uhasselt.be))
