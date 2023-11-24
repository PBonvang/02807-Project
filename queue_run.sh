#!/bin/sh
#BSUB -q hpc
#BSUB -J DBSCAN
#BSUB -n 16
#BSUB -W 4:00
#BSUB -R "rusage[mem=32GB]"
#BSUB -o out/JLOG_%J.out

echo '=================== Load modules: Started ==================='
module load python3
#module load scipy/1.10.1-python-3.11.3
#nvidia-smi
#module load cuda/12.1
echo '=================== Load modules: Succeded ==================='

echo '=================== Activate environment: Start ==================='
source 02807/bin/activate
echo '=================== Activate environment: Succeded ==================='

echo '=================== Executing script: Start ==================='
python3 DBSCAN_clustering.py
echo '=================== Executing script: Succeded ===================