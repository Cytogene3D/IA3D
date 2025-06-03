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
