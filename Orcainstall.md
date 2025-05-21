### Installing the conda orca env

```
git clone https://github.com/jzhoulab/orca.git
cd orca
mamba env create -f orca_env_part1.yml
conda activate orca_env2
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
conda deactivate
mamba env update -f orca_env_part2.yml

```



