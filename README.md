# SwissFEL-BERNINA

Data analysis repository for Time-Resolved X-Ray Diffraction (TR-XRD) experiments at the Bernina intrument of SwissFEL 

Inlcudes code to:
- read data from .json files
- do angular integration
- calculate pump-probe signal

-----------------------------
Installation on a SwissFEL machine

1) First connect to psi server: 

```bash
$ ssh -X ext-perakis_f@hop.psi.ch
```

2) Then connect to the ra-cluster:
```bash 
$ ssh ra
```

3) Make sure to activate bernina conda environment
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
 
4) Then download the repo:

```bash
$ git clone git@github.com:fperakis/SwissFEL-Bernina.git
```

-----------------------------
To run in parallel:

```
salloc -n 12 mpirun ./process.py -r 1 -s 18000
```
with the desired run number (-r integer).

Right now there are some issues:
* you have to specify the number of shots with `-s` or it processes zero shots (bug, will be fixed)
* we cannot submit batch jobs (not sure how to get MPI to play nice with SLURM)

-----------------------------
To submit batch jobs using Slurm do:

```bash
$ cd scripts
$ ./submit_jobs.sh 0001_test # submits run0001_test.json with default parameters
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

and here for information related to SSH:
https://www.psi.ch/computing/ssh

