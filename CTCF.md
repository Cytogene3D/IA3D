
## Identifying the CTFC binding sites

### A site containing almost everything 
https://dozmorovlab.github.io/CTCF

- Install the R package to retrieve _in silico_ predicted binding sites for hg38 (use rtracklayer library to export to bed)

- See section **CTCF predicted and experimental data**:  for Encode data on hg38

### Alternative: Detecting CTCF _manually_ using Fimo
https://meme-suite.org/meme/doc/fimo.html

#### Install Fimo using conda (suggestion)  
https://anaconda.org/bioconda/meme

#### Download the 3 PWM matrices of the CTCF binding sites (JASPAR format)
[all three CTCF PWMs](https://jaspar.genereg.net/search?q=CTCF&collection=all&tax_group=all&tax_id=9606&type=all&class=all&family=all&version=all)

## CFTF in bovine
In the following repository  
  https://web-genobioinfo.toulouse.inrae.fr/~faraut/INIRE  
in data/bed, the _in silico_ predicted CTCF binding sites of the first 32Mb of bovine chromosome 1

The jupyter notebook  
https://web-genobioinfo.toulouse.inrae.fr/~faraut/INIRE/InsulationCompartimentScore.html  
describes the effect of CTCF mutants on interaction maps










