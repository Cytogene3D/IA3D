
Python code to generate random intervals

```python
import random
from intervaltree import IntervalTree

def read_bed(bedfile):
    excluded = IntervalTree()
    with open(bedfile) as f:
        for line in f:
            chrom, start, end = line.strip().split()[:3]
            excluded[int(start):int(end)] = True
    return excluded

def random_intervals(excluded, region_size=32_000_000,  interval_size=312, num_intervals=10000):
    # Generate valid random intervals
    random_intervals = []
    attempts = 0
    while len(random_intervals) < num_intervals and attempts < num_intervals * 10:
        start = random.randint(0, region_size - interval_size)
        end = start + interval_size
        if not excluded.overlaps(start, end):
            random_intervals.append((start, end))
        attempts += 1
    return random_intervals

def dump_intervals(intervals, output):
    with open(output, "w") as out:
        for start, end in intervals:
            out.write(f"chr1\t{start}\t{end}\n")

```
