#!/usr/bin/env -S bash -l
#SBATCH --account=lpt2_sysadmin
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=03:00:00
#SBATCH --mem=20G
#SBATCH --cluster=wice
#SBATCH --mail-user=geertjan.bex@uhasselt.be
#SBATCH --mail-type=END,FAIL

# check whether the script is called with the correct number of arguments, i.e., 1
if [ $# -ne 1 ]
then
    (>&2 echo "Usage: $0 <recipe>")
    exit 1
else
    RECIPE=$1
fi

# check whether the recipe file exists
if [ ! -f $RECIPE ]
then
    (>&2 echo "Recipe file $RECIPE not found")
    exit 2
fi

IMAGE=$(basename "${RECIPE%.*}.sif")

# set and, if necessary, create the directories for the apptainer cache and
# temporary files
export APPTAINER_TMPDIR=$VSC_SCRATCH/singularity_tmp
mkdir -p $APPTAINER_TMPDIR
export APPTAINER_CACHEDIR=$VSC_SCRATCH/singularity_cache
mkdir -p $APPTAINER_CACHEDIR

# build the image
apptainer build --fakeroot $IMAGE $RECIPE
