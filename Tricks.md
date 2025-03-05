# Using Conditional Arguments in `argparse`

In Python's `argparse`, you can enable, require, or restrict arguments based on the presence or value of another argument. Here’s how to do it:

---

## **1. Conditionally Require an Argument**
You can enforce an argument's requirement based on another argument's value using `parser.error()`.

### **Example: Require `--bar` only if `--foo` is "yes"**
```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--foo", choices=["yes", "no"], required=True, help="Enable extra options")
parser.add_argument("--bar", help="Only required if --foo is 'yes'")

args = parser.parse_args()

# Enforce conditional requirement
if args.foo == "yes" and args.bar is None:
    parser.error("--bar is required when --foo is 'yes'")

print(args)
```
## **2. Enable or Restrict Arguments Based on Another Argument
If an argument should only be used when another argument is provided, enforce this manually.

### **Example: --logfile only allowed if --verbose is set
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

