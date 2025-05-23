# Studying the Orca matrices

## The sample matrices

Two sets of matrcices, 
 - observed : corresponding to real HiC data
 - wiltype : Orca predictions made on the same region

```bash
wget https://web-genobioinfo.toulouse.inrae.fr/~faraut/IA3D/observed.tar.gz
wget https://web-genobioinfo.toulouse.inrae.fr/~faraut/IA3D/wildtype.tar.gz
```
Consider recoding the R code in notebooks/OrcaMatrices.ipynb in python

# Working with real data

First download the GSE137372 matrices (micro-C datasets for H1-ESC) and the human genome
```bash
wget https://web-genobioinfo.toulouse.inrae.fr/~faraut/IA3D/4DNFI9GMP2J8.rebinned.mcool
wget https://web-genobioinfo.toulouse.inrae.fr/~faraut/IA3D/Homo_sapiens.GRCh37.75.dna.primary_assembly.fa
```
The matrices are included in a file in mcool format.

Take a look at the notebook Cooltools.ipynb in notebooks.

## Orca predictions for the manuscript Chr9 region

```bash
wget https://web-genobioinfo.toulouse.inrae.fr/~faraut/IA3D/human_ESC.tar.gz
```

## Computing observed over expected matrices

1. By hand
2. Following the implementation of cis_eig
   https://cooltools.readthedocs.io/en/latest/_modules/cooltools/api/eigdecomp.html#cis_eig
3. More simply using the function expected_cis
   https://cooltools.readthedocs.io/en/latest/_modules/cooltools/api/expected.html#expected_cis

see also https://github.com/open2c/open2c_examples/blob/master/contacts_vs_distance.ipynb

