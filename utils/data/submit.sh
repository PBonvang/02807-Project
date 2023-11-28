#!/bin/bash
#BSUB -J VUR
#BSUB -o VUR_LOG_%J.out  
#BSUB -q hpc
#BSUB -W 70:00
#BSUB -R "rusage[mem=8GB]"
#BSUB -n 12
#BSUB -R "span[hosts=1]"
#BSUB -N
# all  BSUB option comments should be above this line!

# execute our command

set -e
pwd
module load python3/3.9.11 #3.7.10
python3 -V

# source ../../.venv/bin/activate
python3 -m pip install -r ../../requirements.txt

python3 scrape.py 2000000 2259957