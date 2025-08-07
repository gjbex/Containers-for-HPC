#!/bin/bash -l
#SBATCH --nodes=1 --ntasks-per-node=1 --cpus-per-task=4
#SBATCH --time=01:00:00
#SBATCH --mem=16G

# fail on error, unset variable, or failed pipe
set -euo pipefail

recipe='
BootStrap: docker
From: continuumio/miniconda3:4.10.3-alpine
Stage: build
%files
    {{ environment_file }} /environment.yml

%post
    . /.singularity.d/env/10-docker*.sh

%post
    cd /
    conda install -c conda-forge conda-pack
    conda env create -n env -f environment.yml
    conda pack -n env -o env.tar.gz

BootStrap: docker
From:  debian:bullseye-slim
Stage: runtime

%post
    . /.singularity.d/env/10-docker*.sh

%files from build
    /env.tar.gz /env.tar.gz

%post
    cd /
    mkdir /env
    cd /env
    tar xzf /env.tar.gz
    cd /
    rm -rv /env.tar.gz
    /env/bin/python /env/bin/conda-unpack

%environment
    export PATH=/env/bin/:$PATH
'

# handle command line arguments
# * --env <environment_file>: name of the environment file to use (required)
# * --sif <container_file>: name of the container file to create (required)
# * --help: show a help message and exit
while [[ $# -gt 0 ]]; do
    case $1 in
        --env)
            if [[ -z "${2:-}" || "${2:0:1}" == "-" ]]; then
                echo "Error: Missing value for --env"
                exit 1
            fi
            environment_file="$2"
            shift 2
            ;;
        --sif)
            if [[ -z "${2:-}" || "${2:0:1}" == "-" ]]; then
                echo "Error: Missing value for --sif"
                exit 1
            fi
            container_file="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 --env <environment_file> --sif <container_file>"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# check that the required arguments are provided
if [[ -z "$environment_file" || -z "$container_file" ]]; then
    echo "Error: --env and --sif options are required."
    exit 1
fi

# check that the environment file exists
if [[ ! -f "$environment_file" ]]; then
    echo "Error: Environment file '$environment_file' does not exist."
    exit 1
fi

# check that the container file does not already exist
if [[ -f "$container_file" ]]; then
    echo "Error: Container file '$container_file' already exists."
    exit 1
fi

# Only when VSC_SCRATCH_NODE is defined do we override Apptainer's tmp dirs;
# otherwise let Apptainer use its own defaults.
if [[ -n "$VSC_SCRATCH_NODE" ]]; then
    if [[ ! -d "$VSC_SCRATCH_NODE" ]]; then
        echo "Error: VSC_SCRATCH_NODE directory '$VSC_SCRATCH_NODE' does not exist."
        exit 1
    fi
    export APPTAINER_TMPDIR="$VSC_SCRATCH_NODE/$USER/apptainer_tmp"
    mkdir -p "$APPTAINER_TMPDIR"
fi
# Only when VSC_SCRATCH is defined do we override Apptainer's cache dirs;
# otherwise let Apptainer use its own defaults.
if [[ -n "$VSC_SCRATCH" ]]; then
    if [[ ! -d "$VSC_SCRATCH" ]]; then
        echo "Error: VSC_SCRATCH directory '$VSC_SCRATCH' does not exist."
        exit 1
    fi
    export APPTAINER_CACHEDIR="$VSC_SCRATCH/apptainer_cache"
    mkdir -p "$APPTAINER_CACHEDIR"
fi

# create the container file
apptainer build \
    --fakeroot \
    --build-arg environment_file="$environment_file" \
    "$container_file" \
    <(printf '%s' "$recipe")
