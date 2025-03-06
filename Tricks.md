# Using Conditional Arguments in `argparse`

In Python's `argparse`, you can enable, require, or restrict arguments based on the presence or value of another argument. Here’s how to do it:

---

## 1. Mutually Exclusive Arguments
If two arguments should not be used together, use add_mutually_exclusive_group().

### Example: --save or --load, but not both
```python
parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--save", action="store_true", help="Save the model")
group.add_argument("--load", action="store_true", help="Load a saved model")

args = parser.parse_args()
print(args)
```

## 2. Enable or Restrict Arguments Based on Another Argument
If an argument should only be used when another argument is provided, enforce this manually.

### Example: --logfile only allowed if --verbose is set
```python
parser = argparse.ArgumentParser()
parser.add_argument("--verbose", action="store_true", help="Enable verbose mode")
parser.add_argument("--logfile", help="Specify a log file (only allowed if --verbose is set)")

args = parser.parse_args()

# Restrict --logfile usage
if args.logfile and not args.verbose:
    parser.error("--logfile can only be used with --verbose")

print(args)
```
# Comparing mutated genome to the original genome

First install blastn in the IA3D env
```
#mamba activate IA3D
mamba install kantorlab::blastn
```
Suppose input.fa is the original fasta sequence and output.fa is the output of the mutate script. 
The blatsn program enables to compare the sequences
```
blastn -query output.fa -subject input.fa -task blastn-short -max_target_seqs 1 -max_hsps 3
```

There is another solution using minimap2 and paftools.js
```
mamba install bioconda::minimap2
```

```
minimap2 -x sr input.fa output.fa --cs=long | paftools.js view -
```

# Controlling reproducibility with random.sample()
In order to control reproductibility, the seed() method is used to initialize the random number generator.
One has to use random.seed() with the same value prior to every invocation of random.sample()

```python
random.seed(3)
random.sample(subseq, len(subseq))
```
Here random.sample() will always return the same "random" sample




