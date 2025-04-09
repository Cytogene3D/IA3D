### Parralelize a python funcion

Suppose we have a python function counting the number of nucleotides of a chromosome

```python
from pysam import FastaFile
def count_nucleotides(genome, chrom):
    with FastaFile(genome) as fasta_handle:
        chromosome = fasta_handle.fetch(chrom)
    return len(chromosome)
    
```
To parrallelize by chromosome use ThreadPoolExecutor from concurrent.futures

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
def parallel_scan(genome, chromosomes):
    results = {}
    num_processes = 4
    with ThreadPoolExecutor(max_workers=num_processes) as executor:
        futures = {executor.submit(count_nucleotides, genome, chrom):chrom for chrom in chromosomes}
        # Collect results
        for future in as_completed(futures):
            chrom = futures[future]
            results[chrom] = future.result()
    return results
```

Take a lookt at
```python
def futures_collector(
    func: Callable,
        argslist: list,
        kwargslist: list[dict] | None = None,
        num_processes: int = cpu_count(),
) -> list:
    """
    Spawns len(arglist) instances of func and executes them at num_processes instances at time.

    * func : a function
    * argslist (list): a list of tuples, arguments of each func
    * kwargslist (list[dict]) a list of dicts, kwargs for each func
    * num_processes (int) : max number of concurrent instances.
        Default : number of available logic cores
    * memory (float|None) : ratio of memory to be used, ranging from .05 to .95. Will not work if *resource* is incompatible.
    """
    if kwargslist is None or len(kwargslist) == len(argslist):
        with ThreadPoolExecutor(max_workers=num_processes) as executor:
            futures = [
                executor.submit(
                    func,
                    *args if isinstance(args, Iterable) else args
                ) if kwargslist is None else
                executor.submit(
                    func,
                    *args if isinstance(args, Iterable) else args,
                    **kwargslist[i]
                ) for i, args in enumerate(argslist)
            ]
        return [f.result() for f in futures]
    else:
        raise ValueError(
            f"""Positionnal argument list length ({len(argslist)})
            does not match keywords argument list length ({len(kwargslist)}).""")
```
from https://github.com/dubssieg/gfagraphs/blob/gfagraphs/pgGraphs/graph.py






