### Installing the conda orca env

```
git clone https://github.com/jzhoulab/orca.git
cd orca
mamba env create -f orca_env_part1.yml
conda activate orca_env
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
conda deactivate
```
### Edit orca_env_part2.yml to remove pytabix before updating

```
mamba env update -f orca_env_part2.yml
```
Now install libstdcxx-ng==13.2.0 then pytabix :
```
conda activate orca_env
mamba install conda-forge::libstdcxx-ng==13.2.0
mamba install pytabix
```




