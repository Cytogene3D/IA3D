## Installation instructions

## Constructing a conda env

Following from the Orca installation instructions  
https://github.com/jzhoulab/orca

### Installing the conda snake orca env

```
mamba env create -f snakeorca_env_part1.yml
mamba activate snakeorca_env
git clone https://github.com/jzhoulab/orca.git
cd orca
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
```

Log on a gpu node and make sure cuda is available
```
srun --mem 16G -p gpuq --gres=gpu:A100_1g.10gb:1 --pty bash
python -c 'import torch; print(torch.cuda.is_available())'
```
The last command should return True

```
conda deactivate
mamba env update -f snakeorca_env_part2.yml
```

Now install libstdcxx-ng==13.2.0 then pytabix :

```
conda activate snakeorca_env
mamba install conda-forge::libstdcxx-ng==13.2.0
mamba install bioconda::pytabix
```


**Installing snakemake**

```
conda activate snakeorca_env
mamba install -c conda-forge -c bioconda snakemake
pip install snakemake-executor-plugin-slurm
```

### Installing SnakeOrca

```
git clone git@forge.inrae.fr:vincent.rocher/snakeorca.git
cd snakeorca
```



## Testing the installation

```
ORCA_DIR=##ROOT_ORCA_DIR##
export PYTHONPATH="$ORCA_DIR":$PYTHONPATH

srun --mem 16G -p gpuq --gres=gpu:A100_1g.10gb:1 --pty bash
python -c 'import torch; print(torch.cuda.is_available())'

```









