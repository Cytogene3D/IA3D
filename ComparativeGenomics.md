## Representative genomes

From Figure 1 in **Toward a genome sequence for every animal: Where are we now?**
https://www.pnas.org/doi/10.1073/pnas.2109019118  

Proposed genomes:
- Human 
- Chimpanzee https://www.ncbi.nlm.nih.gov/datasets/genome/GCA_028858775.3
- Mouse https://github.com/yulab-ql/mhaESC_genome/releases
- Sheep https://www.ncbi.nlm.nih.gov/datasets/genome/GCA_040805955.1
- Goose http://ncbi.nlm.nih.gov/datasets/genome/GCF_040182565.1
- Chinese Sea bass https://www.ncbi.nlm.nih.gov/datasets/genome/GCA_031216445.1
- earthworm (Amynthas aspergillum) https://www.ncbi.nlm.nih.gov/datasets/genome/GCA_049355025.1


## Conserved elements
### PhastCons 
Output from PhastCons can be obtained here  
https://hgdownload.cse.ucsc.edu/goldenPath/hg38/phastCons20way

The hg38.phastCons20way.bw is in bigWig format. This format can be converted to bedgraph format using bigWigToBedGraph:
https://genome.ucsc.edu/goldenpath/help/bigWig.html

On genobioinfo
```
search_module kentUtils
module load bioinfo/kentUtils/472
bigWigToBedGraph -chrom=chr1 hg38.phastCons20way.bw hg38.phastCons20way.chr1.bed
```
Using a python script, chr1.bed is summarized into a conservation score (meand and median) for every non-overlaping window of size 50bp.
