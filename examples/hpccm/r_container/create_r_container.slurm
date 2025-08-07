#!/bin/bash -l
#SBATCH --nodes=1 --ntasks-per-node=1 --cpus-per-task=4
#SBATCH --time=01:00:00
#SBATCH --mem=16G

# fail on error, unset variable, or failed pipe
set -euo pipefail

hpccm_recipe='
# import required modules
import pathlib

# Get the list of apt packages to install
apt_list_filename = USERARG.get("apt_list", "apt_packages.txt")
if not pathlib.Path(apt_list_filename).is_file():
    raise FileNotFoundError(f"File {apt_list_filename} not found.")
with open(apt_list_filename, "r") as apt_file:
    apt_packages = [line.strip() for line in apt_file if line.strip()]

r_package_install_filename = USERARG.get("r_package_install", "install_packages.R")
if not pathlib.Path(r_package_install_filename).is_file():
    raise FileNotFoundError(f"File {r_package_install_filename} not found.")

# Get the base image
image = USERARG.get("baseimage", "ubuntu:22.04")

# Get the bootstrap method
bootstrap = USERARG.get("bootstrap", "docker")
if bootstrap not in ["docker", "localimage"]:
    raise ValueError("Bootstrap method must be either \"docker\" or \"localimage\".")

if bootstrap == "localimage":
    # If using a local image, make sure it exists
    if not pathlib.Path(image).is_file():
        raise FileNotFoundError(f"Local image file {image} does not exist.")

# Choose a base image
Stage0 += baseimage(image=image, _bootstrap=bootstrap)
 
# Set permissions of /tmp
Stage0 += shell(commands=["chmod 1777 /tmp"])

# Install apt packages
if apt_packages:
    Stage0 += apt_get(ospackages=apt_packages)

# Add CRAN repository and signature key
if bootstrap == "docker":
    Stage0 += shell(commands=["wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc | tee -a /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc"])
    Stage0 += shell(commands=["add-apt-repository \"deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/\""])
    Stage0 += shell(commands=["apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 51716619E084DAB9"])

# Install CMake and compiler suite
if bootstrap == "docker":
    Stage0 += cmake(eula=True)
    Stage0 += gnu()

# Install R
if bootstrap == "docker":
    Stage0 += apt_get(ospackages=[
        "r-base",
        "r-base-dev",
        "r-cran-biocmanager",
    ])

# Install R packages
Stage0 += copy(src=r_package_install_filename, dest="/setup/", _mkdir=True)
Stage0 += shell(commands=[f"Rscript /setup/{r_package_install_filename}"])

# Set environment variables
Stage0 += environment(variables={"LC_ALL": "C.UTF-8"})
Stage0 += environment(variables={"TZ": "Europe/Brussels"})

# Add runtime script
Stage0 += runscript(commands=["Rscript"])
'

# handle command line arguments
# * --bootstrap <method>: bootstrap method, either 'docker' or 'localimage' (default: 'docker')
# * --baseimage <image>: name of the base image to use (default: 'ubuntu:22.04')
# * --apt <package_list_file>: name of the file that contains the list of apt packages to install (optional if bootstrapping from a local image)
# * --r-install <r-script>: name of the R script that installs R packages (required)
# * --sif <container_file>: name of the output container file (default: 'r_container.sif')
# * --help: show a help message and exit
while [[ $# -gt 0 ]]; do
    case $1 in
        --bootstrap)
            if [[ -z "${2:-}" || "${2:0:1}" == "-" ]]; then
                echo "Error: Missing value for --bootstrap"
                exit 1
            fi
            bootstrap_method="$2"
            shift 2
            ;;
        --baseimage)
            if [[ -z "${2:-}" || "${2:0:1}" == "-" ]]; then
                echo "Error: Missing value for --baseimage"
                exit 1
            fi
            base_image="$2"
            shift 2
            ;;
        --apt)
            if [[ -z "${2:-}" || "${2:0:1}" == "-" ]]; then
                echo "Error: Missing value for --apt"
                exit 1
            fi
            apt_list_file="$2"
            shift 2
            ;;
        --r-install)
            if [[ -z "${2:-}" || "${2:0:1}" == "-" ]]; then
                echo "Error: Missing value for --r-install"
                exit 1
            fi
            r_install_script="$2"
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
            echo "Usage: $0 --bootstrap <method> --baseimage <image> --apt <package_list_file> --r-install <r_script>"
            echo "Options:"
            echo "  --bootstrap <method>      Bootstrap method, either 'docker' or 'localimage' (default: 'docker')"
            echo "  --baseimage <image>       Name of the base image to use (default: 'ubuntu:22.04')"
            echo "  --apt <package_list_file> Name of the file that contains the list of apt packages to install (optional if bootstrapping from a local image)"
            echo "  --r-install <r_script>    Name of the R script that installs R packages (required)"
            echo "  --sif <container_file>    Name of the output container file (required)"
            echo "  --help                    Show this help message and exit"
            exit 0
            ;;
        *)
            echo "Error: Unknown option '$1'"
            exit 1
            ;;
    esac
done

# check that the container file is provided and is a valid file name
if [[ -z "${container_file:-}" ]]; then
    echo "Error: --sif argument is required."
    exit 1
fi

# if boottrap is given, check that is is either docker or localimage, and set default
if [[ -z "${bootstrap_method:-}" ]]; then
    bootstrap_method="docker"
elif [[ "$bootstrap_method" != "docker" && "$bootstrap_method" != "localimage" ]]; then
    echo "Error: --bootstrap must be either 'docker' or 'localimage'."
    exit 1
fi

# if bootstrap method is localimage, check that the base image is provided, and the file exists
if [[ "$bootstrap_method" == "localimage" ]]; then
    if [[ -z "${base_image:-}" ]]; then
        echo "Error: --baseimage argument is required when using --bootstrap localimage."
        exit 1
    fi
    if [[ ! -f "$base_image" ]]; then
        echo "Error: Base image file '$base_image' does not exist."
        exit 1
    fi
else
    base_image="ubuntu:22.04"
fi

# if bootstrap method is docker, check that the apt list file is provided, and that it exists
if [[ "$bootstrap_method" == "docker" ]]; then
    if [[ -z "${apt_list_file:-}" ]]; then
        echo "Error: --apt argument is required when using --bootstrap docker."
        exit 1
    fi
    if [[ ! -f "$apt_list_file" ]]; then
        echo "Error: Apt package list file '$apt_list_file' does not exist."
        exit 1
    fi
else
    apt_list_file=""
fi

# if the bootstrap method is localimage, and no apt list file is provided, create
# a temporary empty file and assign it to apt_list_file
if [[ "$bootstrap_method" == "localimage" && -z "${apt_list_file:-}" ]]; then
    apt_list_file=$(mktemp)
    echo "No apt packages to install, using an empty file: $apt_list_file"
fi

# check that the R install script is provided and exists
if [[ -z "${r_install_script:-}" ]]; then
    echo "Error: --r-install argument is required."
    exit 1
fi
if [[ ! -f "$r_install_script" ]]; then
    echo "Error: R install script '$r_install_script' does not exist."
    exit 1
fi

# create a Python venv in a temporary directory, activate and install hpccm
echo "Creating python environment and install hpccm..."
venv_dir=$(mktemp -d)
if [[ ! -d "$venv_dir" ]]; then
    echo "Error: Failed to create temporary directory for Python venv."
    exit 1
fi
python3 -m venv "$venv_dir"
source "$venv_dir/bin/activate"
pip install --quiet hpccm

# create the recipe as a temporary file
recipe=$(mktemp)
if [[ ! -f "$recipe" ]]; then
    echo "Error: Failed to create temporary file for the recipe."
    exit 1
fi
# write the hpccm recipe to the temporary file
echo "Generating apptainer recipe..."
hpccm --recipe <(printf '%s' "$hpccm_recipe") \
    --format singularity \
    --userarg apt_list="$apt_list_file" \
    --userarg r_package_install="$r_install_script" \
    --userarg bootstrap="$bootstrap_method" \
    --userarg baseimage="$base_image" > "$recipe"

# Only when VSC_SCRATCH is defined do we override Apptainer's tmp/cache dirs;
# otherwise let Apptainer use its own defaults.
if [[ -n "$VSC_SCRATCH_NODE" ]]; then
    if [[ ! -d "$VSC_SCRATCH_NODE" ]]; then
        echo "Error: VSC_SCRATCH_NODE directory '$VSC_SCRATCH_NODE' does not exist."
        exit 1
    fi
    export APPTAINER_TMPDIR="$VSC_SCRATCH_NODE/$USER/apptainer_tmp"
    mkdir -p "$APPTAINER_TMPDIR"
fi
echo "Using tmp dir: '$APPTAINER_TMPDIR'"
if [[ -n "$VSC_SCRATCH" ]]; then
    if [[ ! -d "$VSC_SCRATCH" ]]; then
        echo "Error: VSC_SCRATCH directory '$VSC_SCRATCH' does not exist."
        exit 1
    fi
    export APPTAINER_CACHEDIR="$VSC_SCRATCH/apptainer_cache"
    mkdir -p "$APPTAINER_CACHEDIR"
fi
echo "Using cache dir: '$APPTAINER_CACHEDIR'"

# create the container file
echo "Building image..."
apptainer build \
    --fakeroot \
    "$container_file" \
    "$recipe"
