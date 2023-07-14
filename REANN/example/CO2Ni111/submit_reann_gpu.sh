#!/bin/sh
#SBATCH --job-name=reann_train

#SBATCH --partition=gpua10
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --time=2-00:00:00

. /etc/profile


# conda environment
conda_env=reann
export OMP_NUM_THREADS=1

#Number of processes per node to launch
NUM_GPUS=var=$(echo $SLURM_STEP_GPUS | awk -F',' '{print NF}')

MASTER=`/bin/hostname -s`


#You will want to replace this
COMMAND="/home/mramos.ifir/tools/REANN/reann/run/train.py"
source $HOME/miniconda3/etc/profile.d/conda.sh
conda activate $conda_env 
python3 -m torch.distributed.run --nproc_per_node=$NUM_GPUS --max_restarts=0 --nnodes=$SLURM_NNODES $COMMAND > out

conda deactivate


