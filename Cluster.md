### The genobioinfo Cluster

https://bioinfo.genotoul.fr

Check https://bioinfo.genotoul.fr/index.php/faq/job_submission_faq

#### Interactive session
The following command will open an interactive session on a cluster node
```
srun --mem 12G --pty bash
```
#### A simple bash script

```bash
#!/bin/bash
#SBATCH -J JobName
#SBATCH -e JobName.err
#SBATCH -o JobName.log
#SBATCH -p workq
#SBATCH --mail-type=END,FAIL
#SBATCH --export=ALL
#SBATCH --cpus-per-task=1    #   CPUS
#SBATCH --mem=8G             #   MEM

# Your command

```


see  also Submit a simple job



