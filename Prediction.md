## Using Orca to predict 3D interactions

Working in a dedicated directory
```
mkdir Orca
cd Orca
```

###  First installing Orca

From https://github.com/jzhoulab/orca

Fist conda env
```
git clone https://github.com/jzhoulab/orca.git
cd orca
mamba env create  -f orca_env_part1.yml
mamba activate orca_env
```
Install pytorch with CUDA 12.4, hence a simple pip command (within orca_env)
```
pip3 install torch torchvision torchaudio
```
Install remaining packages:
```
mamba deactivate
mamba env update -f orca_env_part2.yml
mamba activate orca_env
```
Now Selene
```
git clone https://github.com/kathyxchen/selene.git
cd selene
git checkout custom_target_support
python setup.py build_ext --inplace
python setup.py install 
```

### Testing Orca
A simple test with the process_sequence.py script

First download a 32Mb fasta sequence (first 32Mb of the bovine genome chromosome 1)
(back to the parent Orca dir)
```
mkdir data
cd data
wget https://web-genobioinfo.toulouse.inrae.fr/~faraut/IA3D/bosTau9_chr1_1_32Mb.fa
cd ..
```
Interactive shell on a gpu node, simply to test the installation.\
The command cuda.is_available() checks whether a CUDA-capable GPU is available and can be used.
```
conda activate orca_env
export PYTHONPATH="PATH_TO/Orca/orca":$PYTHONPATH

srun --mem 8G -p gpuq --gres=gpu:A100_1g.10gb:1 --pty bash
python -c 'import torch; print(torch.cuda.is_available())'
```









