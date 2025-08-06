#!/bin/bash -l
#SBATCH --nodes=1 --ntasks-per-node=1 --cpus-per-task=4
#SBATCH --time=01:00:00
#SBATCH --mem=16G

recipe='
BootStrap: docker
From: continuumio/miniconda3:4.10.3-alpine
Stage: build
%post
    . /.singularity.d/env/10-docker*.sh

%post
    cd /
    conda install -c conda-forge conda-pack

%files
    {{ environment_file }} /environment.yml

%post
    cd /
    conda env create -n env -f environment.yml

%post
    cd /
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

%post
    cd /
    rm -rv /env.tar.gz

%post
    cd /
    /env/bin/python /env/bin/conda-unpack

%environment
    export PATH=/env/bin/:$PATH
%post
    export PATH=/env/bin/:$PATH
'

# handle command line arguments
# * --env <enviroment_file>: name of the environment file to use (required)
# * --sif <container_file>: name of the container file to create (required)
# * --help: show a help message and exit
while [[ $# -gt 0 ]]; do
    case $1 in
        --env)
            environment_file="$2"
            shift 2
            ;;
        --sif)
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

# create the container file
apptainer build \
    --fakeroot \
    --build-arg environment_file="$environment_file" \
    "$container_file" \
    <(printf '%s' "$recipe")
