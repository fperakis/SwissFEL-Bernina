# SwissFEL_BERNINA_20181820

Data analysis repository for Time-Resolved X-Ray Diffraction (TR-XRD) experiments at the Bernina intrument of SwissFEL 

Inlcudes code to:
- read data from .json files
- do angular integration
- calculate pump-probe signal

-----------------------------
Installation on a SwissFEL machine

1) ssh to psi: 
ssh -X ext-perakis_f@hop.psi.ch

2) ssh ra

3) activate bernina conda environment
```bash
$ source /sf/bernina/bin/anaconda_env
```

IMPORTANT NOTE: your ~/.bashrc should contain:

```bash
# Source global definitions
if [ -f /etc/bashrc ]; then
        . /etc/bashrc
fi

#Setup the environment for the PSI pmodules
#idocumentation : https://amas.psi.ch/Pmodules
if [ -f /etc/scripts/pmodules.sh ]; then
        . /etc/scripts/pmodules.sh
fi
```
 
4) download the repo:

```bash
$ git clone https://github.com/fperakis/SwissFEL_BERNINA_20181820.git
```

-----------------------------
To run in parallel:

```
salloc -n 12 mpirun ./process.py -r 0069_droplets_10um_2mm -s 18000
```
with the desired run of choice.

Right now there are some issues:
* you have to specify the number of shots with `-s` or it processes zero shots (bug, will be fixed)
* we cannot submit batch jobs (not sure how to get MPI to play nice with SLURM)

-----------------------------
To submit batch jobs using Slurm do:

```bash
$ cd scripts
$ ./submit_jobs.sh 0000_test01 # submits run000_test01 with default parameters
```

For help how to run `submit_jobs.sh`, do: `$ ./submit_jobs.sh`

Useful Slurm commands:

```bash
$ sinfo # check idle nodes
$ squeue -u ext-sellberg_j # check jobs submitted by user 'ext-sellberg_j'
$ scancel 1438285 # kill job with id 1438285
$ sbatch job.sh # to submit job to the default partition, with allocation time of 1 hour
$ sbatch -p week job.sh # to submit to the partition with longer allocation time (2 days if not specified)
$ sbatch -p week -t 4-5:30:00 job.sh # to submit job with time limit of 4 days, 5 hours and 30 minutes (max. allowed time limit is 8 days)
```

See here for more info about computer cluster analysis at SwissFEL:
https://www.psi.ch/photon-science-data-services/offline-computing-facility-for-sls-and-swissfel-data-analysis
