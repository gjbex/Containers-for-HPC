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

if [ -z $RECIPE ]
then
    (>&2 echo "RECIPE not set")
    exit 1
fi

IMAGE=$(basename "${RECIPE%.*}.sif")

export APPTAINER_TMPDIR=$VSC_SCRATCH/singularity_tmp
mkdir -p $APPTAINER_TMPDIR
export APPTAINER_CACHEDIR=$VSC_SCRATCH/singularity_cache
mkdir -p $APPTAINER_CACHEDIR

apptainer build --fakeroot $IMAGE $RECIPE
