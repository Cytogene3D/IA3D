## Using a checkpoint and collect

A proposed solution to compute mutations and predictions only on the valid annotations

```python

checkpoint abs_to_rel:
  input: 
      genome=config["genome"],
      regioninfo="{region}/regioncoordinates.txt"
  output:
      bed=directory({region}/mutations)
  shell:
     python ../scripts/snake_make/compute_all_abs_relative.py --region {input.regioninfo}      

def collect_experiences(wildcards):
    checkpoint_output = checkpoints.abs_to_rel.get(**wildcards).output[0]
    return collect(checkpoint_output, "{{region}}/mutations/{expe}.bed", i=lambda x: ##RECOVER EXPE NAME FROM OUTPUT OF compute_all_abs_relative.py")

rule merge:
    input:
        collect_experiences
    output:
        "{region}/mergedinfos_forregion.txt"
    shell:
        "...."
```


